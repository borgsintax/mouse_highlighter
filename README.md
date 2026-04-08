# 🖱️ Mouse Highlighter

A lightweight Windows tool that renders a coloured translucent halo around the mouse cursor — useful for presentations, screen recordings, tutorials, or anyone who loses track of the pointer on large/multi-monitor setups.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Cursor halo** | Smooth coloured circle that follows the mouse in real time |
| **Click feedback** | Halo turns **red** on left-click, **blue** on right-click |
| **Click-through** | The overlay never intercepts your clicks (Win32 transparent window) |
| **System tray** | Tray icon lets you open Settings or quit without any main window |
| **Settings panel** | Change colour, size and opacity on the fly — no restart needed |
| **Persistent config** | Settings are saved to `config.json` and restored on next launch |
| **Always on top** | Visible above every other window |

---

## 📋 Requirements

- **OS:** Windows 10 / 11 (click-through relies on Win32 APIs)
- **Python:** 3.8 or later (tested up to 3.13)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mouse-highlighter.git
cd mouse-highlighter
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> `tkinter` and `ctypes` ship with the Python standard library — no extra install needed.

---

## ▶️ Running

```bash
python mouse_highlighter.py
```

No main window appears. The app lives entirely in the **system tray** (look for the coloured circle near the clock).

---

## ⚙️ Configuration

**Right-click** the tray icon → **Settings** to open the configuration panel.

| Option | Description | Default |
|---|---|---|
| **Colour** | Halo colour — 8 presets or free colour picker | Yellow (`#FFFF00`) |
| **Size** | Halo radius in pixels | 30 px |
| **Opacity** | Transparency level (0 = invisible, 1 = solid) | 0.3 |

Click **Apply** to save and apply changes immediately. Click **Reset** to restore defaults.

### Configuration files

| File | Purpose | Git |
|---|---|---|
| `config.default.json` | Default values, safe reference point | ✅ committed |
| `config.json` | Your personal settings (auto-created on first Apply) | 🚫 gitignored |

On startup the app loads `config.json` if it exists, otherwise falls back to `config.default.json`.

---

## ❌ Closing the app

The app has no main window by design. Three ways to quit:

1. **Tray** → right-click → **Quit**
2. **F8** key
3. **Escape** key

---

## 📁 Project structure

```
mouse-highlighter/
│
├── mouse_highlighter.py    # Main script
├── config.default.json     # Default settings (committed)
├── config.json             # User settings (gitignored, auto-generated)
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `pystray` | >= 0.19.5 | System tray icon and menu |
| `Pillow` | >= 11.0.0 | Tray icon image generation |
| `tkinter` | built-in | Overlay window and settings UI |
| `ctypes` | built-in | Win32 APIs (click-through, key state) |

---

## ☕ Support

If this tool saves you time, a coffee is always appreciated!

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/odo1969)

---

## 📜 License

MIT — free for personal and commercial use.
