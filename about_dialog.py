"""
about_dialog.py
---------------
Reusable "About" popup template for Python / tkinter projects.
To reuse in another project, just edit the APP_* constants below
and call: AboutDialog(parent_tk_root)
"""

import tkinter as tk
from tkinter import font as tkfont
import webbrowser

# ---------------------------------------------------------------------------
# ✏️  EDIT THESE CONSTANTS FOR EACH PROJECT
# ---------------------------------------------------------------------------
APP_NAME        = "Mouse Highlighter"
APP_VERSION     = "1.0"
APP_DESCRIPTION = "A lightweight overlay that highlights your mouse cursor\nwith a coloured halo — perfect for presentations and recordings."
APP_AUTHOR      = "Francesco Duraccio"
APP_EMAIL       = "francesco.duraccio@gmail.com"
APP_BMC_URL     = "https://buymeacoffee.com/odo1969"
# ---------------------------------------------------------------------------


class AboutDialog:
    """
    Modal About window.

    Usage:
        AboutDialog(parent)          # parent = any tk widget or Tk root
    """

    # Coffee-cup emoji rendered as a small canvas circle (no image files needed)
    _BMC_COLOUR = "#FF813F"   # Buy Me a Coffee brand orange

    def __init__(self, parent: tk.Misc):
        self.win = tk.Toplevel(parent)
        self.win.title(f"About {APP_NAME}")
        self.win.resizable(False, False)
        self.win.attributes("-topmost", True)
        self.win.grab_set()                     # modal
        self.win.configure(bg="#1e1e2e")        # dark background

        self._build_ui()
        self._center(parent)
        self.win.focus_force()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        bg     = "#1e1e2e"
        fg     = "#cdd6f4"
        accent = "#89b4fa"   # soft blue

        # ── App name ──────────────────────────────────────────────────
        big = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        tk.Label(self.win, text=APP_NAME, font=big,
                 bg=bg, fg="#ffffff").pack(pady=(24, 2))

        # ── Version badge ─────────────────────────────────────────────
        tk.Label(self.win, text=f"Version {APP_VERSION}",
                 font=("Segoe UI", 9), bg=bg, fg="#6c7086").pack()

        # ── Divider ───────────────────────────────────────────────────
        tk.Frame(self.win, height=1, bg="#313244").pack(fill="x", padx=24, pady=12)

        # ── Description ───────────────────────────────────────────────
        tk.Label(self.win, text=APP_DESCRIPTION,
                 font=("Segoe UI", 10), bg=bg, fg=fg,
                 justify="center", wraplength=320).pack(padx=24)

        # ── Divider ───────────────────────────────────────────────────
        tk.Frame(self.win, height=1, bg="#313244").pack(fill="x", padx=24, pady=12)

        # ── Author ────────────────────────────────────────────────────
        tk.Label(self.win, text="Author", font=("Segoe UI", 8),
                 bg=bg, fg="#6c7086").pack()
        tk.Label(self.win, text=APP_AUTHOR,
                 font=("Segoe UI", 11, "bold"), bg=bg, fg=fg).pack(pady=(2, 0))

        # ── Email (clickable) ─────────────────────────────────────────
        email_lbl = tk.Label(self.win, text=APP_EMAIL,
                             font=("Segoe UI", 10, "underline"),
                             bg=bg, fg=accent, cursor="hand2")
        email_lbl.pack(pady=(2, 16))
        email_lbl.bind("<Button-1>", lambda e: webbrowser.open(f"mailto:{APP_EMAIL}"))

        # ── Buy Me a Coffee button ─────────────────────────────────────
        bmc_btn = tk.Button(
            self.win,
            text="☕  Buy me a coffee",
            font=("Segoe UI", 10, "bold"),
            bg=self._BMC_COLOUR, fg="#000000",
            activebackground="#e06b2e", activeforeground="#000000",
            relief="flat", bd=0, padx=18, pady=8,
            cursor="hand2",
            command=lambda: webbrowser.open(APP_BMC_URL)
        )
        bmc_btn.pack(pady=(0, 24))

    # ------------------------------------------------------------------
    def _center(self, parent: tk.Misc):
        self.win.update_idletasks()
        w  = self.win.winfo_width()
        h  = self.win.winfo_height()
        try:
            px = parent.winfo_rootx() + parent.winfo_width()  // 2
            py = parent.winfo_rooty() + parent.winfo_height() // 2
        except Exception:
            px = self.win.winfo_screenwidth()  // 2
            py = self.win.winfo_screenheight() // 2
        self.win.geometry(f"+{px - w // 2}+{py - h // 2}")


# ---------------------------------------------------------------------------
# Quick test — run this file directly to preview the dialog
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()          # hide the empty root window
    AboutDialog(root)
    root.mainloop()
