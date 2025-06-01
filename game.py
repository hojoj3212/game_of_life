import curses
import time
import sys

SIZE_X = 80
SIZE_Y = 25

class GameOfLife:
    def __init__(self, filename):
        self.grid = [[0 for _ in range(SIZE_X)] for _ in range(SIZE_Y)]
        self.load_initial_state(filename)
        self.speed = 0.15
        self.cycle = 0

    def load_initial_state(self, filename):
        try:
            with open(filename, 'r') as file:
                for i in range(SIZE_Y):
                    line = file.readline()
                    values = list(map(int, line.strip().split()))
                    for j in range(SIZE_X):
                        self.grid[i][j] = values[j] if j < len(values) else 0
        except FileNotFoundError:
            print(f"File {filename} not found")
            sys.exit(1)

    def count_neighbors(self, i, j):
        count = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                ni, nj = (i + x) % SIZE_Y, (j + y) % SIZE_X
                count += self.grid[ni][nj]
        return count

    def update(self):
        new_grid = [[0 for _ in range(SIZE_X)] for _ in range(SIZE_Y)]
        for i in range(SIZE_Y):
            for j in range(SIZE_X):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j]:
                    new_grid[i][j] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[i][j] = 1 if neighbors == 3 else 0
        
        # Check for stabilization or oscillation
        if self.grid == new_grid:
            return False
        
        self.grid = new_grid
        self.cycle += 1
        return True

    def draw(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Conway's Game of Life")
        stdscr.addstr(1, 0, f"Cycle: {self.cycle} | Speed: {1/self.speed:.1f} FPS (UP/DOWN to adjust)")
        
        for i in range(SIZE_Y):
            for j in range(SIZE_X):
                stdscr.addch(i + 2, j, '*' if self.grid[i][j] else '.')
        
        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(1)
        
        while True:
            self.draw(stdscr)
            
            # Handle input
            key = stdscr.getch()
            if key == curses.KEY_UP:
                self.speed = min(self.speed + 0.01, 1.0)
            elif key == curses.KEY_DOWN:
                self.speed = max(self.speed - 0.01, 0.05)
            elif key == ord('q'):
                break
            
            if not self.update():
                stdscr.nodelay(0)
                stdscr.addstr(SIZE_Y + 3, 0, "All organisms are either dead or stationary. Press any key to exit...")
                stdscr.getch()
                break
            
            time.sleep(self.speed)

def main():
    if len(sys.argv) < 2:
        print("Usage: python game_of_life.py <input_file>")
        sys.exit(1)
    
    game = GameOfLife(sys.argv[1])
    curses.wrapper(game.run)

if __name__ == "__main__":
    main()
