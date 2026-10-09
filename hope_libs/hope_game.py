# hope_game.py HopeLang v1.5.2 游戏扩展库，纯标准库tkinter
# hope_game.py 适配修复版，不返回布尔，返回1/0数字
import tkinter
import time

_game = {
    "root": None,
    "canvas": None,
    "opened": False,
    "key_state": dict(),
    "mouse_x": 0.0,
    "mouse_y": 0.0,
    "mouse_left": 0,
    "mouse_right": 0,
    "last_tick": 0.0
}

def _game_init(args):
    width = float(args[0])
    height = float(args[1])
    win_title = str(args[2])
    if _game["root"] is not None:
        return None
    root = tkinter.Tk()
    root.title(win_title)
    canvas = tkinter.Canvas(root, width=int(width), height=int(height), bg="#000000")
    canvas.pack()

    def key_down_cb(event):
        _game["key_state"][event.keysym.upper()] = True
    def key_up_cb(event):
        _game["key_state"][event.keysym.upper()] = False

    def mouse_move_cb(event):
        _game["mouse_x"] = event.x
        _game["mouse_y"] = event.y

    def mouse_left_down(event):
        _game["mouse_left"] = 1
    def mouse_left_up(event):
        _game["mouse_left"] = 0
    def mouse_right_down(event):
        _game["mouse_right"] = 1
    def mouse_right_up(event):
        _game["mouse_right"] = 0

    root.bind("<KeyPress>", key_down_cb)
    root.bind("<KeyRelease>", key_up_cb)
    canvas.bind("<Motion>", mouse_move_cb)
    canvas.bind("<Button-1>", mouse_left_down)
    canvas.bind("<ButtonRelease-1>", mouse_left_up)
    canvas.bind("<Button-3>", mouse_right_down)
    canvas.bind("<ButtonRelease-3>", mouse_right_up)

    _game["root"] = root
    _game["canvas"] = canvas
    _game["opened"] = True
    _game["last_tick"] = time.perf_counter()
    return None

def _game_is_open(args):
    return 1 if _game["opened"] else 0

# ============新增：主动关闭窗口API game_close()============
def _game_close(args):
    if _game["root"] is not None:
        try:
            _game["root"].destroy()
        except tkinter.TclError:
            pass
    _game["opened"] = False
    _game["root"] = None
    _game["canvas"] = None
    return None

def _game_delta_time(args):
    now = time.perf_counter()
    dt = now - _game["last_tick"]
    _game["last_tick"] = now
    return dt

def _game_clear(args):
    r = float(args[0])
    g = float(args[1])
    b = float(args[2])
    if r <= 1.0 and g <= 1.0 and b <= 1.0:
        r *= 255
        g *= 255
        b *= 255
    rr = max(0, min(255, int(r)))
    gg = max(0, min(255, int(g)))
    bb = max(0, min(255, int(b)))
    if not _game["opened"]:
        return None
    hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
    c = _game["canvas"]
    c.delete("all")
    c.configure(bg=hex_color)
    return None

def _game_draw_rect(args):
    x = float(args[0])
    y = float(args[1])
    w = float(args[2])
    h = float(args[3])
    r = float(args[4])
    g = float(args[5])
    b = float(args[6])
    if r <=1.0 and g <=1.0 and b <=1.0:
        r *=255
        g *=255
        b *=255
    rr = max(0, min(255, int(r)))
    gg = max(0, min(255, int(g)))
    bb = max(0, min(255, int(b)))
    if not _game["opened"]:
        return None
    c = _game["canvas"]
    hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
    c.create_rectangle(x, y, x+w, y+h, fill=hex_color, outline="")
    return None

def _game_draw_circle(args):
    cx = float(args[0])
    cy = float(args[1])
    radius = float(args[2])
    r = float(args[3])
    g = float(args[4])
    b = float(args[5])
    if r <=1.0 and g <=1.0 and b <=1.0:
        r *=255
        g *=255
        b *=255
    rr = max(0, min(255, int(r)))
    gg = max(0, min(255, int(g)))
    bb = max(0, min(255, int(b)))
    if not _game["opened"]:
        return None
    c = _game["canvas"]
    hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
    x1 = cx - radius
    y1 = cy - radius
    x2 = cx + radius
    y2 = cy + radius
    c.create_oval(x1, y1, x2, y2, fill=hex_color, outline="")
    return None

def _game_draw_text(args):
    x = float(args[0])
    y = float(args[1])
    text = str(args[2])
    size = int(args[3])
    r = float(args[4])
    g = float(args[5])
    b = float(args[6])
    if r <=1.0 and g <=1.0 and b <=1.0:
        r *=255
        g *=255
        b *=255
    rr = max(0, min(255, int(r)))
    gg = max(0, min(255, int(g)))
    bb = max(0, min(255, int(b)))
    if not _game["opened"]:
        return None
    c = _game["canvas"]
    hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
    c.create_text(x, y, text=text, font=("Consolas", size), fill=hex_color)
    return None

def _game_mouse_x(args):
    return _game["mouse_x"]
def _game_mouse_y(args):
    return _game["mouse_y"]

def _game_mouse_down(args):
    btn = str(args[0]).upper()
    if btn == "LEFT":
        return _game["mouse_left"]
    elif btn == "RIGHT":
        return _game["mouse_right"]
    return 0

def _game_aabb_collide(args):
    x1 = float(args[0])
    y1 = float(args[1])
    w1 = float(args[2])
    h1 = float(args[3])
    x2 = float(args[4])
    y2 = float(args[5])
    w2 = float(args[6])
    h2 = float(args[7])
    collide = not (
        x1 + w1 < x2 or
        x2 + w2 < x1 or
        y1 + h1 < y2 or
        y2 + h2 < y1
    )
    return 1 if collide else 0

def _game_key_down(args):
    key_name = str(args[0]).upper()
    return 1 if _game["key_state"].get(key_name, False) else 0

def _game_present(args):
    # 只有窗口有效才执行update，防止销毁后继续调用
    if not _game["opened"] or _game["root"] is None:
        return None
    try:
        _game["root"].update()
    except tkinter.TclError:
        _game["opened"] = False
        _game["root"] = None
        _game["canvas"] = None
    return None

HOPE_EXPORT = {
    "game_init":        (["width", "height", "title"], _game_init),
    "game_close":       ([], _game_close),   # 新增关闭窗口
    "game_is_open":     ([], _game_is_open),
    "game_delta_time":  ([], _game_delta_time),
    "game_clear":       (["r", "g", "b"], _game_clear),
    "game_draw_rect":   (["x", "y", "w", "h", "r", "g", "b"], _game_draw_rect),
    "game_draw_circle": (["cx", "cy", "radius", "r", "g", "b"], _game_draw_circle),
    "game_draw_text":   (["x", "y", "text", "size", "r", "g", "b"], _game_draw_text),
    "game_mouse_x":     ([], _game_mouse_x),
    "game_mouse_y":     ([], _game_mouse_y),
    "game_mouse_down":  (["button"], _game_mouse_down),
    "game_aabb_collide":(["x1","y1","w1","h1","x2","y2","w2","h2"], _game_aabb_collide),
    "game_key_down":    (["key"], _game_key_down),
    "game_present":     ([], _game_present)
}




