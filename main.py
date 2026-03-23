import time
import pyautogui
from screen_reader import locate_grid
from config import ROWS, COLS

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.02

def compute_grid():
    anchors = locate_grid()
    if not anchors:
        return None

    tl, br = anchors

    grid_left   = tl.left
    grid_top    = tl.top
    grid_right  = br.left + br.width
    grid_bottom = br.top  + br.height

    grid_width  = grid_right - grid_left
    grid_height = grid_bottom - grid_top

    cell_w = grid_width  / COLS
    cell_h = grid_height / ROWS

    return grid_left, grid_top, cell_w, cell_h


def cell_to_screen(r, c, grid_left, grid_top, cell_w, cell_h):
    x = grid_left + c * cell_w + cell_w / 2
    y = grid_top  + r * cell_h + cell_h / 2
    return int(x), int(y)


def right_click_all_cells():
    grid = compute_grid()
    if not grid:
        print("Grid not found.")
        return

    grid_left, grid_top, cell_w, cell_h = grid

    print("Starting in 3 seconds...")
    time.sleep(3)

    for r in range(ROWS):
        for c in range(COLS):
            x, y = cell_to_screen(r, c, grid_left, grid_top, cell_w, cell_h)

            pyautogui.moveTo(x, y, duration=0.05)
            pyautogui.click(button='right')

    print("Done.")


if __name__ == "__main__":
    right_click_all_cells()