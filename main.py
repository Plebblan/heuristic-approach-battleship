import pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05
import time

print("Hover over TOP-LEFT cell...")
time.sleep(5)
x1, y1 = pyautogui.position()
print("Top-left:", x1, y1)

print("Hover over BOTTOM-RIGHT cell...")
time.sleep(5)
x2, y2 = pyautogui.position()
print("Bottom-right:", x2, y2)

width = x2 - x1
height = y2 - y1
print("Grid size:", width, height)