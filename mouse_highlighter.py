import tkinter as tk
from tkinter import colorchooser, ttk
import ctypes
import platform
import threading
import json
import os

from about_dialog import AboutDialog

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "pillow"])
    import pystray
    from PIL import Image, ImageDraw


# ---------------------------------------------------------------------------
# Config paths
# ---------------------------------------------------------------------------
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH  = os.path.join(BASE_DIR, "config.json")
DEFAULT_PATH = os.path.join(BASE_DIR, "config.default.json")

DEFAULT_CONFIG = {"color": "#FFFF00", "alpha": 0.3, "radius": 30}


def load_config() -> dict:
    """Load user config; fall back to config.default.json, then hardcoded defaults."""
    for path in (CONFIG_PATH, DEFAULT_PATH):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {**DEFAULT_CONFIG, **data}
            except (json.JSONDecodeError, OSError):
                pass
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    """Persist settings to config.json (gitignored)."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except OSError as e:
        print(f"Could not save config: {e}")


# ---------------------------------------------------------------------------
# Preset colours
# ---------------------------------------------------------------------------
PRESET_COLORS = [
    ("🟡 Yellow",  "#FFFF00"),
    ("🔴 Red",     "#FF4444"),
    ("🟢 Green",   "#44FF44"),
    ("🔵 Blue",    "#4488FF"),
    ("🟠 Orange",  "#FF8800"),
    ("🟣 Purple",  "#CC44FF"),
    ("⚪ White",   "#FFFFFF"),
    ("🩷 Pink",    "#FF69B4"),
]


# ---------------------------------------------------------------------------
# Settings window
# ---------------------------------------------------------------------------
class SettingsWindow:
    """Configuration panel opened from the tray menu."""

    def __init__(self, app: "MouseHighlighter"):
        self.app = app

        if hasattr(self.app, "_settings_win") and self.app._settings_win is not None:
            try:
                self.app._settings_win.win.lift()
                return
            except Exception:
                pass

        self.win = tk.Toplevel(self.app.root)
        self.win.title("Mouse Highlighter — Settings")
        self.win.resizable(False, False)
        self.win.attributes("-topmost", True)
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)
        self.app._settings_win = self

        self._build_ui()
        self._center_window()

    def _build_ui(self):
        pad = dict(padx=12, pady=6)

        # --- Colour ---
        frm_color = ttk.LabelFrame(self.win, text="Highlight colour", padding=8)
        frm_color.grid(row=0, column=0, sticky="ew", **pad)

        self._color_var = tk.StringVar(value=self.app.color)

        for idx, (label, hexcol) in enumerate(PRESET_COLORS):
            tk.Button(
                frm_color, text=label, width=12, relief="ridge", cursor="hand2",
                command=lambda c=hexcol: self._set_color(c)
            ).grid(row=idx // 4, column=idx % 4, padx=4, pady=3)

        tk.Button(
            frm_color, text="🎨  Custom colour…", width=28,
            command=self._pick_custom_color, cursor="hand2"
        ).grid(row=2, column=0, columnspan=4, pady=(6, 2))

        self._preview = tk.Label(
            frm_color, text="  Current colour  ",
            bg=self.app.color, relief="solid", width=20, height=1
        )
        self._preview.grid(row=3, column=0, columnspan=4, pady=(4, 0))

        # --- Size ---
        frm_size = ttk.LabelFrame(self.win, text="Size (radius in px)", padding=8)
        frm_size.grid(row=1, column=0, sticky="ew", **pad)

        self._radius_var = tk.IntVar(value=self.app.radius)
        self._radius_lbl = tk.Label(frm_size, text=f"{self.app.radius} px", width=6)
        self._radius_lbl.pack(side="right")
        tk.Scale(
            frm_size, from_=10, to=100, orient="horizontal",
            variable=self._radius_var, length=260,
            command=lambda v: self._radius_lbl.config(text=f"{int(float(v))} px")
        ).pack(side="left", fill="x", expand=True)

        # --- Opacity ---
        frm_alpha = ttk.LabelFrame(self.win, text="Opacity  (0 = invisible  →  1 = solid)", padding=8)
        frm_alpha.grid(row=2, column=0, sticky="ew", **pad)

        self._alpha_var = tk.DoubleVar(value=self.app.alpha)
        self._alpha_lbl = tk.Label(frm_alpha, text=f"{self.app.alpha:.2f}", width=6)
        self._alpha_lbl.pack(side="right")
        tk.Scale(
            frm_alpha, from_=0.05, to=1.0, resolution=0.05, orient="horizontal",
            variable=self._alpha_var, length=260,
            command=lambda v: self._alpha_lbl.config(text=f"{float(v):.2f}")
        ).pack(side="left", fill="x", expand=True)

        # --- Buttons ---
        frm_btn = tk.Frame(self.win)
        frm_btn.grid(row=3, column=0, pady=(4, 12))

        tk.Button(frm_btn, text="✅  Apply",  width=14, command=self._apply,    cursor="hand2").pack(side="left", padx=8)
        tk.Button(frm_btn, text="↩️  Reset",  width=14, command=self._reset,    cursor="hand2").pack(side="left", padx=8)
        tk.Button(frm_btn, text="❌  Close",  width=14, command=self._on_close, cursor="hand2").pack(side="left", padx=8)

    def _center_window(self):
        self.win.update_idletasks()
        w  = self.win.winfo_width()
        h  = self.win.winfo_height()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    def _set_color(self, hexcol: str):
        self._color_var.set(hexcol)
        self._preview.config(bg=hexcol)

    def _pick_custom_color(self):
        result = colorchooser.askcolor(color=self._color_var.get(),
                                       title="Pick a colour", parent=self.win)
        if result and result[1]:
            self._set_color(result[1])

    def _apply(self):
        self.app.color  = self._color_var.get()
        self.app.alpha  = self._alpha_var.get()
        self.app.radius = self._radius_var.get()
        self.app.apply_settings(save=True)

    def _reset(self):
        cfg = dict(DEFAULT_CONFIG)
        self._set_color(cfg["color"])
        self._radius_var.set(cfg["radius"])
        self._radius_lbl.config(text=f"{cfg['radius']} px")
        self._alpha_var.set(cfg["alpha"])
        self._alpha_lbl.config(text=f"{cfg['alpha']:.2f}")

    def _on_close(self):
        self.app._settings_win = None
        self.win.destroy()


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------
class MouseHighlighter:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mouse Highlighter")
        self._running      = True
        self._settings_win = None

        cfg         = load_config()
        self.color  = cfg["color"]
        self.alpha  = cfg["alpha"]
        self.radius = cfg["radius"]

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self._rebuild_canvas()

        if platform.system() == "Windows":
            self._make_click_through()

        self.tray_icon = self._create_tray_icon()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

        self.root.bind("<Escape>", lambda e: self.quit())
        self._update_position()

    # ------------------------------------------------------------------
    def _rebuild_canvas(self):
        size = self.radius * 2
        self.root.geometry(f"{size}x{size}")
        self.root.attributes("-alpha", self.alpha)

        if hasattr(self, "canvas"):
            self.canvas.destroy()

        self.canvas = tk.Canvas(
            self.root, width=size, height=size,
            bg="white", highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.create_oval(
            0, 0, size, size,
            fill=self.color, outline=self.color, width=0
        )

    def apply_settings(self, save: bool = False):
        self._rebuild_canvas()
        try:
            self.tray_icon.icon = self._make_tray_image()
        except Exception:
            pass
        if save:
            save_config({"color": self.color, "alpha": self.alpha, "radius": self.radius})

    # ------------------------------------------------------------------
    def _make_tray_image(self) -> Image.Image:
        img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        h    = self.color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        border  = (max(r - 60, 0), max(g - 60, 0), max(b - 60, 0), 255)
        draw.ellipse((4, 4, 60, 60), fill=(r, g, b, 255), outline=border, width=3)
        return img

    def _create_tray_icon(self) -> pystray.Icon:
        menu = pystray.Menu(
            pystray.MenuItem("Mouse Highlighter", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⚙️  Settings", self._on_tray_settings),
            pystray.MenuItem("❓  About",    self._on_tray_about),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌  Quit",     self._on_tray_quit),
        )
        return pystray.Icon(
            name="MouseHighlighter",
            icon=self._make_tray_image(),
            title="Mouse Highlighter",
            menu=menu,
        )

    def _on_tray_about(self, icon, item):
        self.root.after(0, lambda: AboutDialog(self.root))

    def _on_tray_settings(self, icon, item):
        self.root.after(0, lambda: SettingsWindow(self))

    def _on_tray_quit(self, icon, item):
        icon.stop()
        self.root.after(0, self.quit)

    # ------------------------------------------------------------------
    def _make_click_through(self):
        try:
            self.root.update()
            GWL_EXSTYLE       = -20
            WS_EX_LAYERED     = 0x80000
            WS_EX_TRANSPARENT = 0x20
            hwnd  = ctypes.windll.user32.GetParent(self.root.winfo_id()) or self.root.winfo_id()
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(
                hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            )
        except Exception as e:
            print(f"Click-through error: {e}")

    # ------------------------------------------------------------------
    def _update_position(self):
        if not self._running:
            return
        try:
            x, y = self.root.winfo_pointerxy()
            self.root.geometry(f"+{x - self.radius}+{y - self.radius}")

            left  = ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000
            right = ctypes.windll.user32.GetAsyncKeyState(0x02) & 0x8000

            if left:
                self.canvas.itemconfig(1, fill="red",      outline="red",      width=0)
            elif right:
                self.canvas.itemconfig(1, fill="blue",     outline="blue",     width=4)
            else:
                self.canvas.itemconfig(1, fill=self.color, outline=self.color, width=0)

            if ctypes.windll.user32.GetAsyncKeyState(0x77) & 0x8000:   # F8
                self.quit()
                return

        except Exception:
            pass

        self.root.after(10, self._update_position)

    def quit(self):
        self._running = False
        try:
            self.tray_icon.stop()
        except Exception:
            pass
        self.root.destroy()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app  = MouseHighlighter(root)
    root.mainloop()
