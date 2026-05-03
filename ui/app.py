import tkinter as tk
from tkinter import ttk

import ui.styles as styles
from ui.index_tab import IndexTab
from ui.collection_tab import CollectionTab


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metal Fight Beyblade Collection Tracker")
        self.geometry("1100x720")
        self.minsize(900, 600)

        styles.apply(self)
        self._build_ui()
        self._center_window()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header bar ───────────────────────────────────────────────────────
        header = tk.Frame(self, bg=styles.C["bg_dark"], height=52)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="⚙  METAL FIGHT BEYBLADE",
            bg=styles.C["bg_dark"],
            fg=styles.C["accent"],
            font=styles.F["h1"],
        ).pack(side="left", padx=20, pady=0)

        tk.Label(
            header,
            text="Collection Tracker",
            bg=styles.C["bg_dark"],
            fg=styles.C["text_sub"],
            font=styles.F["h3"],
        ).pack(side="left", padx=(0, 20), pady=0)

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # ── Notebook ──────────────────────────────────────────────────────────
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill="both", expand=True)

        self._collection_tab = CollectionTab(self._notebook)
        self._index_tab = IndexTab(self._notebook,
                                   on_collection_change=self._collection_tab.refresh)

        self._notebook.add(self._index_tab,      text="  Beyblade Index  ")
        self._notebook.add(self._collection_tab, text="  My Collection   ")

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w)//2}+{(sh - h)//2}")
