import tkinter as tk
from tkinter import ttk

# ── Palette (GitHub dark / Catppuccin-inspired) ───────────────────────────────
C = {
    "bg_dark":      "#0d1117",
    "bg_main":      "#161b22",
    "bg_surface":   "#21262d",
    "bg_hover":     "#30363d",
    "bg_input":     "#0d1117",
    "border":       "#30363d",
    "accent":       "#58a6ff",
    "accent_light": "#79c0ff",
    "gold":         "#e3b341",
    "text":         "#e6edf3",
    "text_sub":     "#8b949e",
    "text_muted":   "#6e7681",
    "attack":       "#f85149",
    "defense":      "#58a6ff",
    "stamina":      "#3fb950",
    "balance":      "#e3b341",
    "success":      "#3fb950",
    "danger":       "#f85149",
}

TYPE_COLOR = {
    "Attack":  C["attack"],
    "Defense": C["defense"],
    "Stamina": C["stamina"],
    "Balance": C["balance"],
}

FONT_FAMILY = "Segoe UI"
F = {
    "h1":    (FONT_FAMILY, 22, "bold"),
    "h2":    (FONT_FAMILY, 14, "bold"),
    "h3":    (FONT_FAMILY, 11, "bold"),
    "body":  (FONT_FAMILY, 10),
    "small": (FONT_FAMILY, 9),
    "mono":  ("Consolas", 9),
}


def apply(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Base ──────────────────────────────────────────────────────────────────
    style.configure(".",
        background=C["bg_main"],
        foreground=C["text"],
        font=F["body"],
        borderwidth=0,
        relief="flat",
        focuscolor=C["accent"],
    )

    # ── Frame ─────────────────────────────────────────────────────────────────
    style.configure("TFrame",    background=C["bg_main"])
    style.configure("Dark.TFrame",    background=C["bg_dark"])
    style.configure("Surface.TFrame", background=C["bg_surface"])
    style.configure("Card.TFrame",    background=C["bg_surface"])

    # ── Label ─────────────────────────────────────────────────────────────────
    style.configure("TLabel",      background=C["bg_main"], foreground=C["text"],     font=F["body"])
    style.configure("H1.TLabel",   background=C["bg_main"], foreground=C["text"],     font=F["h1"])
    style.configure("H2.TLabel",   background=C["bg_main"], foreground=C["text"],     font=F["h2"])
    style.configure("H3.TLabel",   background=C["bg_main"], foreground=C["text"],     font=F["h3"])
    style.configure("Muted.TLabel",background=C["bg_main"], foreground=C["text_sub"], font=F["small"])
    style.configure("Gold.TLabel", background=C["bg_main"], foreground=C["gold"],     font=F["h2"])

    # Surface-backed labels (inside cards)
    for name, bg in (("Surface", C["bg_surface"]), ("Dark", C["bg_dark"])):
        style.configure(f"{name}.TLabel",      background=bg, foreground=C["text"],     font=F["body"])
        style.configure(f"{name}.H2.TLabel",   background=bg, foreground=C["text"],     font=F["h2"])
        style.configure(f"{name}.H3.TLabel",   background=bg, foreground=C["text"],     font=F["h3"])
        style.configure(f"{name}.Muted.TLabel",background=bg, foreground=C["text_sub"], font=F["small"])

    # ── Notebook ──────────────────────────────────────────────────────────────
    style.configure("TNotebook",
        background=C["bg_dark"],
        tabmargins=[0, 0, 0, 0],
        borderwidth=0,
    )
    style.configure("TNotebook.Tab",
        background=C["bg_surface"],
        foreground=C["text_sub"],
        padding=[24, 10],
        font=F["h3"],
        borderwidth=0,
    )
    style.map("TNotebook.Tab",
        background=[("selected", C["bg_main"]), ("active", C["bg_hover"])],
        foreground=[("selected", C["accent"]),  ("active", C["text"])],
    )

    # ── Treeview ──────────────────────────────────────────────────────────────
    style.configure("Treeview",
        background=C["bg_surface"],
        foreground=C["text"],
        fieldbackground=C["bg_surface"],
        rowheight=30,
        font=F["body"],
        borderwidth=0,
        relief="flat",
    )
    style.configure("Treeview.Heading",
        background=C["bg_dark"],
        foreground=C["text_sub"],
        font=F["h3"],
        relief="flat",
        borderwidth=0,
    )
    style.map("Treeview",
        background=[("selected", C["accent"])],
        foreground=[("selected", "#ffffff")],
    )
    style.map("Treeview.Heading",
        background=[("active", C["bg_hover"])],
    )

    # ── Scrollbar ─────────────────────────────────────────────────────────────
    style.configure("Vertical.TScrollbar",
        background=C["bg_hover"],
        troughcolor=C["bg_dark"],
        arrowcolor=C["text_muted"],
        borderwidth=0,
        arrowsize=10,
    )
    style.map("Vertical.TScrollbar",
        background=[("active", C["text_muted"])],
    )

    # ── Entry ─────────────────────────────────────────────────────────────────
    style.configure("TEntry",
        fieldbackground=C["bg_input"],
        foreground=C["text"],
        insertcolor=C["text"],
        selectbackground=C["accent"],
        borderwidth=1,
        relief="solid",
        padding=[6, 4],
    )

    # ── Combobox ──────────────────────────────────────────────────────────────
    style.configure("TCombobox",
        fieldbackground=C["bg_input"],
        background=C["bg_surface"],
        foreground=C["text"],
        selectbackground=C["accent"],
        arrowcolor=C["text_sub"],
        borderwidth=1,
        relief="solid",
        padding=[6, 4],
    )
    style.map("TCombobox",
        fieldbackground=[("readonly", C["bg_input"])],
        foreground=[("readonly", C["text"])],
    )

    # ── Spinbox ───────────────────────────────────────────────────────────────
    style.configure("TSpinbox",
        fieldbackground=C["bg_input"],
        background=C["bg_surface"],
        foreground=C["text"],
        insertcolor=C["text"],
        arrowcolor=C["text_sub"],
        borderwidth=1,
        relief="solid",
        padding=[6, 4],
    )

    # ── Button ────────────────────────────────────────────────────────────────
    style.configure("TButton",
        background=C["bg_surface"],
        foreground=C["text"],
        font=F["h3"],
        padding=[14, 7],
        relief="flat",
        borderwidth=0,
    )
    style.map("TButton",
        background=[("active", C["bg_hover"]), ("pressed", C["bg_dark"])],
        relief=[("pressed", "flat")],
    )

    style.configure("Accent.TButton",
        background=C["accent"],
        foreground="#ffffff",
        font=F["h3"],
        padding=[14, 7],
    )
    style.map("Accent.TButton",
        background=[("active", C["accent_light"]), ("pressed", C["accent"])],
    )

    style.configure("Success.TButton",
        background=C["success"],
        foreground="#ffffff",
        font=F["h3"],
        padding=[14, 7],
    )
    style.map("Success.TButton",
        background=[("active", "#4ade80"), ("pressed", C["success"])],
    )

    style.configure("Danger.TButton",
        background=C["danger"],
        foreground="#ffffff",
        font=F["h3"],
        padding=[14, 7],
    )
    style.map("Danger.TButton",
        background=[("active", "#ff6b6b"), ("pressed", C["danger"])],
    )

    style.configure("Small.TButton",
        background=C["bg_surface"],
        foreground=C["text"],
        font=F["small"],
        padding=[8, 4],
    )
    style.map("Small.TButton",
        background=[("active", C["bg_hover"])],
    )

    # ── Separator ─────────────────────────────────────────────────────────────
    style.configure("TSeparator", background=C["border"])

    # root window background
    root.configure(bg=C["bg_dark"])
