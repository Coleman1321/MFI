import tkinter as tk
from tkinter import ttk, messagebox

import db.database as db
from ui.styles import C, F, TYPE_COLOR


class CollectionTab(ttk.Frame):
    def __init__(self, parent: ttk.Notebook):
        super().__init__(parent, style="TFrame")
        self._entries = []
        self._selected_cid: int | None = None

        self._build_ui()
        self.refresh()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_header()
        self._build_list()
        self._build_controls()
        self._build_summary()

    def _build_header(self):
        hdr = ttk.Frame(self, style="Dark.TFrame")
        hdr.grid(row=0, column=0, sticky="ew")

        ttk.Label(hdr, text="My Collection", style="Dark.H2.TLabel"
                  ).pack(side="left", padx=16, pady=10)

        self._total_lbl = ttk.Label(hdr, text="", style="Dark.Muted.TLabel")
        self._total_lbl.pack(side="right", padx=16)

    def _build_list(self):
        frame = ttk.Frame(self, style="TFrame")
        frame.grid(row=1, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        cols = ("name", "series", "type", "qty")
        self._tree = ttk.Treeview(frame, columns=cols, show="headings",
                                  selectmode="browse")
        self._tree.heading("name",   text="Name",     anchor="w")
        self._tree.heading("series", text="Series",   anchor="w")
        self._tree.heading("type",   text="Type",     anchor="center")
        self._tree.heading("qty",    text="Qty",      anchor="center")

        self._tree.column("name",   width=280, stretch=True,  anchor="w")
        self._tree.column("series", width=130, stretch=False, anchor="w")
        self._tree.column("type",   width=80,  stretch=False, anchor="center")
        self._tree.column("qty",    width=60,  stretch=False, anchor="center")

        for t, col in TYPE_COLOR.items():
            self._tree.tag_configure(t, foreground=col)
        self._tree.tag_configure("odd",  background=C["bg_surface"])
        self._tree.tag_configure("even", background="#1c2128")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _build_controls(self):
        bar = ttk.Frame(self, style="Surface.TFrame")
        bar.grid(row=2, column=0, sticky="ew")

        self._dec_btn = ttk.Button(bar, text="−", style="Small.TButton",
                                   command=self._decrement, width=3)
        self._dec_btn.pack(side="left", padx=(12, 2), pady=8)

        self._qty_lbl = tk.Label(bar, text="0", width=4, anchor="center",
                                 bg=C["bg_surface"], fg=C["text"],
                                 font=F["h3"])
        self._qty_lbl.pack(side="left", padx=2)

        self._inc_btn = ttk.Button(bar, text="＋", style="Small.TButton",
                                   command=self._increment, width=3)
        self._inc_btn.pack(side="left", padx=(2, 16), pady=8)

        self._remove_btn = ttk.Button(bar, text="Remove from Collection",
                                      style="Danger.TButton",
                                      command=self._remove)
        self._remove_btn.pack(side="right", padx=12, pady=8)

        self._selected_name = ttk.Label(bar, text="No item selected",
                                        style="Surface.Muted.TLabel")
        self._selected_name.pack(side="left", pady=8)

        self._set_controls_state(False)

    def _build_summary(self):
        summary = ttk.Frame(self, style="Dark.TFrame")
        summary.grid(row=3, column=0, sticky="ew")

        # Stat tiles
        self._stat_total  = self._make_tile(summary, "Total",   C["accent"])
        self._stat_attack  = self._make_tile(summary, "Attack",  C["attack"])
        self._stat_defense = self._make_tile(summary, "Defense", C["defense"])
        self._stat_stamina = self._make_tile(summary, "Stamina", C["stamina"])
        self._stat_balance = self._make_tile(summary, "Balance", C["balance"])

    def _make_tile(self, parent, label, color) -> tk.Label:
        tile = tk.Frame(parent, bg=C["bg_surface"], padx=16, pady=10)
        tile.pack(side="left", padx=(12, 0), pady=10)

        tk.Label(tile, text=label, bg=C["bg_surface"],
                 fg=color, font=F["small"]).pack()
        val = tk.Label(tile, text="0", bg=C["bg_surface"],
                       fg=C["text"], font=F["h2"])
        val.pack()
        return val

    # ── Data ──────────────────────────────────────────────────────────────────

    def refresh(self):
        self._entries = db.get_collection()
        self._populate_tree()
        self._refresh_summary()
        self._selected_cid = None
        self._set_controls_state(False)

    def _populate_tree(self):
        self._tree.delete(*self._tree.get_children())
        for i, e in enumerate(self._entries):
            tags = (e.bey_type, "even" if i % 2 == 0 else "odd")
            self._tree.insert("", "end", iid=str(e.id),
                              values=(e.name, e.series, e.bey_type, e.quantity),
                              tags=tags)

    def _refresh_summary(self):
        s = db.get_collection_summary()
        self._stat_total.config( text=str(s["total"]))
        self._stat_attack.config( text=str(s["attack"]))
        self._stat_defense.config(text=str(s["defense"]))
        self._stat_stamina.config(text=str(s["stamina"]))
        self._stat_balance.config(text=str(s["balance"]))
        n = len(self._entries)
        self._total_lbl.config(text=f"{n} unique · {s['total']} total")

    def _on_select(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            return
        cid = int(sel[0])
        self._selected_cid = cid
        entry = next((e for e in self._entries if e.id == cid), None)
        if entry:
            self._qty_lbl.config(text=str(entry.quantity))
            self._selected_name.config(text=entry.name)
            self._set_controls_state(True)

    def _set_controls_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for w in (self._dec_btn, self._inc_btn, self._remove_btn):
            w.config(state=state)
        if not enabled:
            self._qty_lbl.config(text="—")
            self._selected_name.config(text="No item selected")

    def _entry(self):
        return next((e for e in self._entries if e.id == self._selected_cid), None)

    def _increment(self):
        e = self._entry()
        if not e:
            return
        new_qty = e.quantity + 1
        db.update_quantity(e.id, new_qty)
        self._qty_lbl.config(text=str(new_qty))
        e.quantity = new_qty
        self._tree.set(str(e.id), "qty", new_qty)
        self._refresh_summary()

    def _decrement(self):
        e = self._entry()
        if not e:
            return
        if e.quantity <= 1:
            if messagebox.askyesno(
                "Remove",
                f'Quantity is 1. Remove "{e.name}" from collection?',
            ):
                self._remove()
            return
        new_qty = e.quantity - 1
        db.update_quantity(e.id, new_qty)
        self._qty_lbl.config(text=str(new_qty))
        e.quantity = new_qty
        self._tree.set(str(e.id), "qty", new_qty)
        self._refresh_summary()

    def _remove(self):
        e = self._entry()
        if not e:
            return
        if messagebox.askyesno("Confirm Remove",
                               f'Remove "{e.name}" from your collection?'):
            db.remove_from_collection(e.id)
            self.refresh()
