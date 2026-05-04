import tkinter as tk
from tkinter import ttk, messagebox

import db.database as db
from ui.styles import C, F, TYPE_COLOR


SPIN_SYMBOL = {"Right": "↻", "Left": "↺", "Both": "⇄"}
ERA_COLOR   = {
    "Pre-Hybrid": "#8b949e",
    "Hybrid":     "#58a6ff",
    "4D":         "#cba6f7",
    "Zero-G":     "#3fb950",
}


class IndexTab(ttk.Frame):
    def __init__(self, parent: ttk.Notebook, on_collection_change):
        super().__init__(parent, style="TFrame")
        self._on_collection_change = on_collection_change
        self._beyblades = []
        self._selected_id: int | None = None

        # Load persisted setting
        self._show_variants = tk.BooleanVar(
            value=db.get_setting("show_variants", "true") == "true"
        )
        self._show_variants.trace_add("write", self._on_variants_toggle)

        self._build_ui()
        self.refresh()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        self._build_toolbar()
        self._build_list()
        self._build_detail()

    def _build_toolbar(self):
        bar = ttk.Frame(self, style="Dark.TFrame")
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Search
        ttk.Label(bar, text="🔍", style="Dark.TLabel",
                  font=F["h3"]).pack(side="left", padx=(12, 4), pady=10)
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        ttk.Entry(bar, textvariable=self._search_var,
                  width=22).pack(side="left", pady=10, padx=(0, 12))

        # Era filter
        ttk.Label(bar, text="Era", style="Dark.Muted.TLabel").pack(side="left", padx=(0, 4))
        self._era_var = tk.StringVar(value="All")
        era_cb = ttk.Combobox(bar, textvariable=self._era_var,
                              values=db.ERA_OPTIONS, state="readonly", width=11)
        era_cb.pack(side="left", pady=10, padx=(0, 12))
        era_cb.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        # Series filter
        ttk.Label(bar, text="Series", style="Dark.Muted.TLabel").pack(side="left", padx=(0, 4))
        self._series_var = tk.StringVar(value="All")
        series_cb = ttk.Combobox(bar, textvariable=self._series_var,
                                 values=db.SERIES_OPTIONS, state="readonly", width=13)
        series_cb.pack(side="left", pady=10, padx=(0, 12))
        series_cb.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        # Type filter
        ttk.Label(bar, text="Type", style="Dark.Muted.TLabel").pack(side="left", padx=(0, 4))
        self._type_var = tk.StringVar(value="All")
        type_cb = ttk.Combobox(bar, textvariable=self._type_var,
                                values=db.TYPE_OPTIONS, state="readonly", width=9)
        type_cb.pack(side="left", pady=10, padx=(0, 12))
        type_cb.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        # Show Variants toggle
        ttk.Checkbutton(
            bar, text="Show Variants",
            variable=self._show_variants,
            style="TCheckbutton",
        ).pack(side="left", pady=10, padx=(4, 0))

        self._count_lbl = ttk.Label(bar, text="", style="Dark.Muted.TLabel")
        self._count_lbl.pack(side="right", padx=12)

    def _build_list(self):
        frame = ttk.Frame(self, style="TFrame")
        frame.grid(row=1, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        cols = ("bb", "name", "series", "type", "spin")
        self._tree = ttk.Treeview(frame, columns=cols, show="headings",
                                  selectmode="browse")
        self._tree.heading("bb",     text="BB #",   anchor="w")
        self._tree.heading("name",   text="Name",   anchor="w")
        self._tree.heading("series", text="Series", anchor="w")
        self._tree.heading("type",   text="Type",   anchor="center")
        self._tree.heading("spin",   text="Spin",   anchor="center")

        self._tree.column("bb",     width=72,  stretch=False, anchor="w")
        self._tree.column("name",   width=220, stretch=True,  anchor="w")
        self._tree.column("series", width=120, stretch=False, anchor="w")
        self._tree.column("type",   width=72,  stretch=False, anchor="center")
        self._tree.column("spin",   width=46,  stretch=False, anchor="center")

        for t, col in TYPE_COLOR.items():
            self._tree.tag_configure(t, foreground=col)
        self._tree.tag_configure("odd",  background=C["bg_surface"])
        self._tree.tag_configure("even", background="#1c2128")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)
        self._tree.bind("<Double-1>", self._on_double_click)

    def _build_detail(self):
        outer = ttk.Frame(self, style="Surface.TFrame")
        outer.grid(row=1, column=1, sticky="nsew", padx=(1, 0))
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)

        canvas = tk.Canvas(outer, bg=C["bg_surface"], highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self._detail_frame = ttk.Frame(canvas, style="Surface.TFrame")
        self._detail_win = canvas.create_window((0, 0), window=self._detail_frame,
                                                anchor="nw")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(self._detail_win, width=e.width))
        self._detail_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Placeholder
        self._placeholder = ttk.Label(
            self._detail_frame,
            text="Select a Beyblade\nto see details",
            style="Surface.Muted.TLabel",
            justify="center",
        )
        self._placeholder.pack(pady=60)

        # ── Detail body ───────────────────────────────────────────────────────
        self._detail_body = ttk.Frame(self._detail_frame, style="Surface.TFrame")

        # BB number + name
        self._bb_lbl = ttk.Label(self._detail_body, style="Surface.Muted.TLabel")
        self._bb_lbl.pack(anchor="w", padx=20, pady=(16, 0))

        self._name_lbl = ttk.Label(self._detail_body, style="Surface.H2.TLabel",
                                   wraplength=280, justify="left")
        self._name_lbl.pack(anchor="w", padx=20, pady=(2, 4))

        # Badges row
        self._badges = tk.Frame(self._detail_body, bg=C["bg_surface"])
        self._badges.pack(anchor="w", padx=20, pady=(0, 4))
        self._type_badge  = self._make_badge(self._badges, C["bg_surface"])
        self._type_badge.pack(side="left", padx=(0, 6))
        self._spin_badge  = self._make_badge(self._badges, C["bg_hover"])
        self._spin_badge.pack(side="left", padx=(0, 6))
        self._era_badge   = self._make_badge(self._badges, C["bg_hover"])
        self._era_badge.pack(side="left")

        # Meta row
        self._meta_lbl = ttk.Label(self._detail_body, style="Surface.Muted.TLabel",
                                   wraplength=280, justify="left")
        self._meta_lbl.pack(anchor="w", padx=20, pady=(0, 2))

        self._variant_lbl = ttk.Label(self._detail_body, style="Surface.Muted.TLabel",
                                      wraplength=280, justify="left", font=F["small"])
        self._variant_lbl.pack(anchor="w", padx=20)

        ttk.Separator(self._detail_body, orient="horizontal").pack(
            fill="x", padx=20, pady=10)

        # Parts breakdown
        parts = [
            ("Face Bolt",      "_fb_lbl"),
            ("Energy Ring",    "_er_lbl"),
            ("Fusion Wheel",   "_fw_lbl"),
            ("Spin Track",     "_st_lbl"),
            ("Perf. Tip",      "_pt_lbl"),
        ]
        for label, attr in parts:
            row = ttk.Frame(self._detail_body, style="Surface.TFrame")
            row.pack(fill="x", padx=20, pady=2)
            ttk.Label(row, text=label + ":", style="Surface.Muted.TLabel",
                      width=14, anchor="w").pack(side="left")
            lbl = ttk.Label(row, text="", style="Surface.TLabel")
            lbl.pack(side="left")
            setattr(self, attr, lbl)

        ttk.Separator(self._detail_body, orient="horizontal").pack(
            fill="x", padx=20, pady=10)

        # Qty + Add
        qty_frame = ttk.Frame(self._detail_body, style="Surface.TFrame")
        qty_frame.pack(fill="x", padx=20, pady=4)
        ttk.Label(qty_frame, text="Qty:", style="Surface.TLabel").pack(side="left", padx=(0, 6))
        self._qty_var = tk.IntVar(value=1)
        ttk.Spinbox(qty_frame, from_=1, to=99, textvariable=self._qty_var,
                    width=5).pack(side="left")

        self._add_btn = ttk.Button(
            self._detail_body, text="＋  Add to Collection",
            style="Accent.TButton", command=self._add_to_collection,
        )
        self._add_btn.pack(fill="x", padx=20, pady=(8, 20))

    @staticmethod
    def _make_badge(parent, bg) -> tk.Label:
        return tk.Label(parent, text="", bg=bg, fg="#ffffff",
                        font=F["small"], padx=8, pady=2, relief="flat")

    # ── Data ──────────────────────────────────────────────────────────────────

    def refresh(self):
        self._beyblades = db.get_all_beyblades(
            search=self._search_var.get().strip(),
            era=self._era_var.get(),
            series=self._series_var.get(),
            bey_type=self._type_var.get(),
            show_variants=self._show_variants.get(),
        )
        self._populate_tree()

    def _populate_tree(self):
        self._tree.delete(*self._tree.get_children())
        for i, b in enumerate(self._beyblades):
            spin_sym = SPIN_SYMBOL.get(b.spin_direction, b.spin_direction)
            tags = (b.bey_type, "even" if i % 2 == 0 else "odd")
            self._tree.insert("", "end", iid=str(b.id),
                              values=(b.bb_number, b.name, b.series,
                                      b.bey_type, spin_sym),
                              tags=tags)
        self._count_lbl.config(text=f"{len(self._beyblades)} entries")

    def _on_select(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            return
        bey_id = int(sel[0])
        self._selected_id = bey_id
        bey = next((b for b in self._beyblades if b.id == bey_id), None)
        if bey:
            self._show_detail(bey)

    def _on_double_click(self, _event=None):
        self._add_to_collection()

    def _on_variants_toggle(self, *_):
        db.set_setting("show_variants",
                       "true" if self._show_variants.get() else "false")
        self.refresh()

    def _show_detail(self, bey):
        self._placeholder.pack_forget()
        self._detail_body.pack(fill="both", expand=True)

        self._bb_lbl.config(text=f"{bey.bb_number}  ·  {bey.release_type}")
        self._name_lbl.config(text=bey.name)

        type_color = TYPE_COLOR.get(bey.bey_type, C["text"])
        self._type_badge.config(text=f" {bey.bey_type} ", bg=type_color)

        spin_sym = SPIN_SYMBOL.get(bey.spin_direction, bey.spin_direction)
        self._spin_badge.config(text=f" {spin_sym} {bey.spin_direction} ")

        era_color = ERA_COLOR.get(bey.era, C["text_sub"])
        self._era_badge.config(text=f" {bey.era} ", bg=era_color)

        date_str = bey.release_date or "Date unknown"
        self._meta_lbl.config(text=f"{bey.series}  ·  {date_str}")

        if bey.variant_note:
            self._variant_lbl.config(text=f"Variant: {bey.variant_note}")
        else:
            self._variant_lbl.config(text="")

        self._fb_lbl.config(text=bey.face_bolt)
        self._er_lbl.config(text=bey.energy_ring)
        self._fw_lbl.config(text=bey.fusion_wheel)
        self._st_lbl.config(text=bey.spin_track)
        self._pt_lbl.config(text=bey.performance_tip)

        self._qty_var.set(1)

    def _add_to_collection(self):
        if self._selected_id is None:
            messagebox.showinfo("No Selection", "Please select a Beyblade first.")
            return
        qty = max(1, self._qty_var.get())
        db.add_to_collection(self._selected_id, qty)
        bey = next((b for b in self._beyblades if b.id == self._selected_id), None)
        name = bey.name if bey else "Beyblade"
        messagebox.showinfo("Added", f'"{name}" added to your collection!')
        self._on_collection_change()
