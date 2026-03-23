import re
import time
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from matplotlib.patches import Wedge, Rectangle, Circle

def get_detailed_input(url):
    options = Options()
    # Mở trình duyệt để theo dõi
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3) 
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    game_div = soup.find('div', id='game')
    all_divs = game_div.find_all('div', class_='cell')
    
    # 1. Tách biệt ô chơi (Play) và ô số (Task)
    play_cells = [c for c in all_divs if 'task' not in c.get('class', [])]
    
    # Nhóm tọa độ lưới để tránh lệch pixel
    def get_grid_coords(cells, attr):
        raw = sorted(list(set(int(re.search(fr'{attr}:\s*(\d+)px', c['style']).group(1)) for c in cells)))
        if not raw: return []
        final = [raw[0]]
        for i in range(1, len(raw)):
            if raw[i] - final[-1] > 10: final.append(raw[i])
        return final

    all_lefts = get_grid_coords(play_cells, 'left')
    all_tops = get_grid_coords(play_cells, 'top')
    size = len(all_tops)

    def get_idx(val, target_list):
        return min(range(len(target_list)), key=lambda i: abs(target_list[i] - val))

    row_hints, col_hints = [0]*size, [0]*size
    fixed_map = {} # (r, col) -> (Type, is_locked)

    for c in all_divs:
        cls = c.get('class', [])
        cls_str = " ".join(cls)
        style = c.get('style', '')
        left = int(re.search(r'left:\s*(\d+)px', style).group(1))
        top = int(re.search(r'top:\s*(\d+)px', style).group(1))

        if 'task' in cls:
            val = int(c.text)
            if 'v' in cls: col_hints[get_idx(left, all_lefts)] = val
            else: row_hints[get_idx(top, all_tops)] = val
        else:
            r, col = get_idx(top, all_tops), get_idx(left, all_lefts)
            
            # Kiểm tra trạng thái bị khóa (LOCKED)
            is_locked = 'locked' in cls
            
            # Phân loại mảnh tàu
            part = 'EMPTY'
            if 'water' in cls_str: part = 'WATER'
            elif 'ship-single' in cls_str: part = 'SINGLE'
            elif 'ship-t' in cls_str: part = 'TOP'
            elif 'ship-b' in cls_str: part = 'BOTTOM'
            elif 'ship-l' in cls_str: part = 'LEFT'
            elif 'ship-r' in cls_str: part = 'RIGHT'
            elif 'ship-m' in cls_str or ('ship' in cls_str and 'cell-on' in cls_str): 
                part = 'MIDDLE'

            if part != 'EMPTY':
                fixed_map[(r, col)] = (part, is_locked)

    driver.quit()
    return size, row_hints, col_hints, fixed_map

def draw_study_board(size, rows, cols, fixed):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1, size)
    ax.set_ylim(-1, size + 1)
    
    for i in range(size + 1):
        ax.axhline(i, color='black', lw=2)
        ax.axvline(i, color='black', lw=2)
        
    for i, val in enumerate(rows):
        ax.text(-0.5, size - i - 0.5, str(val), va='center', ha='center', fontsize=14, fontweight='bold')
    for i, val in enumerate(cols):
        ax.text(i + 0.5, size + 0.5, str(val), va='center', ha='center', fontsize=14, fontweight='bold')
        
    for (r, col), (part, is_locked) in fixed.items():
        y, x = size - r - 1, col
        color = 'black'
        # Đánh dấu ô bị khóa bằng viền đỏ
        edge = 'red' if is_locked else 'none'
        lw = 2 if is_locked else 0

        if part == 'WATER':
            ax.add_patch(Rectangle((x, y), 1, 1, color='#E0F7FA'))
            ax.text(x+0.5, y+0.5, "~", color='#00BCD4', va='center', ha='center', fontsize=20)
        elif part == 'SINGLE':
            ax.add_patch(Circle((x+0.5, y+0.5), 0.35, color=color, ec=edge, lw=lw))
        elif part == 'MIDDLE':
            ax.add_patch(Rectangle((x+0.15, y+0.15), 0.7, 0.7, color=color, ec=edge, lw=lw))
        elif part == 'TOP':
            ax.add_patch(Wedge((x+0.5, y+0.25), 0.4, 0, 180, color=color, ec=edge, lw=lw))
        elif part == 'BOTTOM':
            ax.add_patch(Wedge((x+0.5, y+0.75), 0.4, 180, 360, color=color, ec=edge, lw=lw))
        elif part == 'LEFT':
            ax.add_patch(Wedge((x+0.75, y+0.5), 0.4, 90, 270, color=color, ec=edge, lw=lw))
        elif part == 'RIGHT':
            ax.add_patch(Wedge((x+0.25, y+0.5), 0.4, 270, 450, color=color, ec=edge, lw=lw))

    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.title("DỮ LIỆU BÀN CỜ (VIỀN ĐỎ LÀ Ô BỊ KHÓA)", pad=20, fontsize=15)
    plt.show()

# --- CHẠY CHƯƠNG TRÌNH ---
URL = "https://www.puzzle-battleships.com/?size=1" 
size, rows, cols, fixed = get_detailed_input(URL)
draw_study_board(size, rows, cols, fixed)