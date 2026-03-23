import pyautogui

def locate_grid():
    print("Locating grid anchors...")

    tl = pyautogui.locateOnScreen(
        "input/templates/grid_top_left_corner.png",
        confidence=0.9
    )

    br = pyautogui.locateOnScreen(
        "input/templates/grid_bot_right_corner.png",
        confidence=0.9
    )

    if not tl or not br:
        print("Could not find both corners.")
        return None

    print("Anchors found")
    return tl, br