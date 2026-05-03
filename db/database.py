import sqlite3
import sys
from pathlib import Path
from typing import List, Optional

from models.beyblade import Beyblade
from models.collection import CollectionEntry


def get_db_path() -> Path:
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent.parent
    return app_dir / "collection.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(get_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db() -> None:
    conn = _connect()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS beyblades (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT    NOT NULL,
            series          TEXT    NOT NULL,
            bey_type        TEXT    NOT NULL,
            face_bolt       TEXT    NOT NULL,
            energy_ring     TEXT    NOT NULL,
            fusion_wheel    TEXT    NOT NULL,
            spin_track      TEXT    NOT NULL,
            performance_tip TEXT    NOT NULL,
            image_path      TEXT
        );

        CREATE TABLE IF NOT EXISTS collection (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            beyblade_id  INTEGER NOT NULL REFERENCES beyblades(id) ON DELETE CASCADE,
            quantity     INTEGER NOT NULL DEFAULT 1
        );
    """)

    cur.execute("SELECT COUNT(*) FROM beyblades")
    if cur.fetchone()[0] == 0:
        from db.seed_data import BEYBLADES
        cur.executemany(
            """INSERT INTO beyblades
               (name, series, bey_type, face_bolt, energy_ring,
                fusion_wheel, spin_track, performance_tip)
               VALUES (?,?,?,?,?,?,?,?)""",
            BEYBLADES,
        )

    conn.commit()
    conn.close()


# ── Beyblade index queries ────────────────────────────────────────────────────

def get_all_beyblades(
    search: str = "",
    series: str = "All",
    bey_type: str = "All",
) -> List[Beyblade]:
    conn = _connect()
    cur = conn.cursor()

    query = "SELECT * FROM beyblades WHERE 1=1"
    params: list = []

    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")
    if series and series != "All":
        query += " AND series = ?"
        params.append(series)
    if bey_type and bey_type != "All":
        query += " AND bey_type = ?"
        params.append(bey_type)

    query += " ORDER BY series, name"
    rows = cur.execute(query, params).fetchall()
    conn.close()
    return [_row_to_beyblade(r) for r in rows]


def get_beyblade_by_id(beyblade_id: int) -> Optional[Beyblade]:
    conn = _connect()
    cur = conn.cursor()
    row = cur.execute("SELECT * FROM beyblades WHERE id=?", (beyblade_id,)).fetchone()
    conn.close()
    return _row_to_beyblade(row) if row else None


def _row_to_beyblade(row: sqlite3.Row) -> Beyblade:
    return Beyblade(
        id=row["id"],
        name=row["name"],
        series=row["series"],
        bey_type=row["bey_type"],
        face_bolt=row["face_bolt"],
        energy_ring=row["energy_ring"],
        fusion_wheel=row["fusion_wheel"],
        spin_track=row["spin_track"],
        performance_tip=row["performance_tip"],
        image_path=row["image_path"],
    )


# ── Collection queries ────────────────────────────────────────────────────────

def get_collection() -> List[CollectionEntry]:
    conn = _connect()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT c.id, c.beyblade_id, c.quantity,
               b.name, b.series, b.bey_type,
               b.face_bolt, b.energy_ring, b.fusion_wheel,
               b.spin_track, b.performance_tip
        FROM collection c
        JOIN beyblades b ON b.id = c.beyblade_id
        ORDER BY b.series, b.name
    """).fetchall()
    conn.close()
    return [_row_to_entry(r) for r in rows]


def _row_to_entry(row: sqlite3.Row) -> CollectionEntry:
    return CollectionEntry(
        id=row["id"],
        beyblade_id=row["beyblade_id"],
        quantity=row["quantity"],
        name=row["name"],
        series=row["series"],
        bey_type=row["bey_type"],
        face_bolt=row["face_bolt"],
        energy_ring=row["energy_ring"],
        fusion_wheel=row["fusion_wheel"],
        spin_track=row["spin_track"],
        performance_tip=row["performance_tip"],
    )


def is_in_collection(beyblade_id: int) -> Optional[int]:
    """Return collection row id if already owned, else None."""
    conn = _connect()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM collection WHERE beyblade_id=?", (beyblade_id,)
    ).fetchone()
    conn.close()
    return row["id"] if row else None


def add_to_collection(beyblade_id: int, quantity: int = 1) -> None:
    existing_id = is_in_collection(beyblade_id)
    conn = _connect()
    if existing_id is not None:
        conn.execute(
            "UPDATE collection SET quantity = quantity + ? WHERE id = ?",
            (quantity, existing_id),
        )
    else:
        conn.execute(
            "INSERT INTO collection (beyblade_id, quantity) VALUES (?,?)",
            (beyblade_id, quantity),
        )
    conn.commit()
    conn.close()


def update_quantity(collection_id: int, quantity: int) -> None:
    if quantity < 1:
        return
    conn = _connect()
    conn.execute(
        "UPDATE collection SET quantity=? WHERE id=?", (quantity, collection_id)
    )
    conn.commit()
    conn.close()


def remove_from_collection(collection_id: int) -> None:
    conn = _connect()
    conn.execute("DELETE FROM collection WHERE id=?", (collection_id,))
    conn.commit()
    conn.close()


def get_collection_summary() -> dict:
    conn = _connect()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT COALESCE(SUM(quantity),0) FROM collection"
    ).fetchone()
    total = row[0]

    rows = cur.execute("""
        SELECT b.bey_type, COALESCE(SUM(c.quantity),0)
        FROM collection c
        JOIN beyblades b ON b.id = c.beyblade_id
        GROUP BY b.bey_type
    """).fetchall()
    conn.close()

    by_type = {r[0]: r[1] for r in rows}
    return {
        "total": total,
        "attack": by_type.get("Attack", 0),
        "defense": by_type.get("Defense", 0),
        "stamina": by_type.get("Stamina", 0),
        "balance": by_type.get("Balance", 0),
    }


SERIES_OPTIONS = ["All", "Metal Fusion", "Metal Masters", "Metal Fury"]
TYPE_OPTIONS = ["All", "Attack", "Defense", "Stamina", "Balance"]
