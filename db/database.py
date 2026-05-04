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


# ── Schema ────────────────────────────────────────────────────────────────────

_CREATE_BEYBLADES = """
    CREATE TABLE IF NOT EXISTS beyblades (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        bb_number       TEXT    NOT NULL DEFAULT '',
        name            TEXT    NOT NULL,
        era             TEXT    NOT NULL DEFAULT '',
        series          TEXT    NOT NULL,
        release_type    TEXT    NOT NULL DEFAULT 'Booster',
        variant_note    TEXT    NOT NULL DEFAULT '',
        bey_type        TEXT    NOT NULL,
        spin_direction  TEXT    NOT NULL DEFAULT 'Right',
        release_date    TEXT,
        face_bolt       TEXT    NOT NULL DEFAULT '',
        energy_ring     TEXT    NOT NULL DEFAULT '',
        fusion_wheel    TEXT    NOT NULL DEFAULT '',
        spin_track      TEXT    NOT NULL DEFAULT '',
        performance_tip TEXT    NOT NULL DEFAULT '',
        image_path      TEXT
    );
"""

_CREATE_COLLECTION = """
    CREATE TABLE IF NOT EXISTS collection (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        beyblade_id  INTEGER NOT NULL REFERENCES beyblades(id) ON DELETE CASCADE,
        quantity     INTEGER NOT NULL DEFAULT 1
    );
"""

_CREATE_RANDOM_BOOSTERS = """
    CREATE TABLE IF NOT EXISTS random_boosters (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        bb_number    TEXT    NOT NULL,
        name         TEXT    NOT NULL,
        era          TEXT    NOT NULL
    );
    CREATE TABLE IF NOT EXISTS random_booster_contents (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        booster_id   INTEGER NOT NULL REFERENCES random_boosters(id) ON DELETE CASCADE,
        possible_bey TEXT    NOT NULL,
        is_rare      INTEGER NOT NULL DEFAULT 0
    );
"""

_CREATE_SETTINGS = """
    CREATE TABLE IF NOT EXISTS settings (
        key   TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
"""

# Columns added after the initial release — used for in-place migration.
_NEW_COLUMNS = {
    "bb_number":      "TEXT NOT NULL DEFAULT ''",
    "era":            "TEXT NOT NULL DEFAULT ''",
    "release_type":   "TEXT NOT NULL DEFAULT 'Booster'",
    "variant_note":   "TEXT NOT NULL DEFAULT ''",
    "spin_direction": "TEXT NOT NULL DEFAULT 'Right'",
    "release_date":   "TEXT",
}


def _migrate_beyblades(conn: sqlite3.Connection) -> None:
    """Add any new columns that don't yet exist (safe, non-destructive)."""
    cur = conn.cursor()
    existing = {row[1] for row in cur.execute("PRAGMA table_info(beyblades)").fetchall()}
    for col, typedef in _NEW_COLUMNS.items():
        if col not in existing:
            conn.execute(f"ALTER TABLE beyblades ADD COLUMN {col} {typedef}")
    conn.commit()


def initialize_db() -> None:
    conn = _connect()
    cur = conn.cursor()

    # Create tables
    cur.executescript(
        _CREATE_BEYBLADES
        + _CREATE_COLLECTION
        + _CREATE_RANDOM_BOOSTERS
        + _CREATE_SETTINGS
    )

    # Migrate existing schema if needed
    _migrate_beyblades(conn)

    # Default settings
    conn.execute(
        "INSERT OR IGNORE INTO settings (key, value) VALUES ('show_variants', 'true')"
    )

    # Seed beyblades on first run (or when the table is empty)
    cur.execute("SELECT COUNT(*) FROM beyblades")
    if cur.fetchone()[0] == 0:
        _seed_beyblades(conn)
        _seed_random_boosters(conn)

    conn.commit()

    # Startup log
    cur.execute("SELECT COUNT(*) FROM beyblades")
    total = cur.fetchone()[0]
    print(f"[MFB Tracker] Loaded {total} beyblades into index.")

    conn.close()


def _seed_beyblades(conn: sqlite3.Connection) -> None:
    from db.seed_data import BEYBLADES
    conn.executemany(
        """INSERT INTO beyblades
           (bb_number, name, era, series, release_type, variant_note,
            bey_type, spin_direction, release_date,
            face_bolt, energy_ring, fusion_wheel, spin_track, performance_tip)
           VALUES
           (:bb_number, :name, :era, :series, :release_type, :variant_note,
            :bey_type, :spin_direction, :release_date,
            :face_bolt, :energy_ring, :fusion_wheel, :spin_track, :performance_tip)""",
        BEYBLADES,
    )


def _seed_random_boosters(conn: sqlite3.Connection) -> None:
    from db.seed_data import RANDOM_BOOSTERS
    for rb in RANDOM_BOOSTERS:
        cur = conn.execute(
            "INSERT INTO random_boosters (bb_number, name, era) VALUES (?,?,?)",
            (rb["bb_number"], rb["name"], rb["era"]),
        )
        booster_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO random_booster_contents (booster_id, possible_bey, is_rare) VALUES (?,?,?)",
            [(booster_id, c["possible_bey"], c["is_rare"]) for c in rb["contents"]],
        )


# ── Settings ──────────────────────────────────────────────────────────────────

def get_setting(key: str, default: str = "") -> str:
    conn = _connect()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    conn = _connect()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()
    conn.close()


# ── Beyblade index queries ────────────────────────────────────────────────────

def get_all_beyblades(
    search: str = "",
    era: str = "All",
    series: str = "All",
    bey_type: str = "All",
    show_variants: bool = True,
) -> List[Beyblade]:
    conn = _connect()
    cur = conn.cursor()

    if show_variants:
        query = "SELECT * FROM beyblades WHERE 1=1"
    else:
        # One row per unique name — pick the earliest bb_number per name.
        query = """
            SELECT * FROM beyblades
            WHERE id IN (
                SELECT MIN(id) FROM beyblades GROUP BY name
            )
            AND 1=1
        """

    params: list = []

    if search:
        query += " AND (name LIKE ? OR bb_number LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if era and era != "All":
        query += " AND era = ?"
        params.append(era)
    if series and series != "All":
        query += " AND series = ?"
        params.append(series)
    if bey_type and bey_type != "All":
        query += " AND bey_type = ?"
        params.append(bey_type)

    query += " ORDER BY bb_number, name"
    rows = cur.execute(query, params).fetchall()
    conn.close()
    return [_row_to_beyblade(r) for r in rows]


def get_beyblade_by_id(beyblade_id: int) -> Optional[Beyblade]:
    conn = _connect()
    row = conn.execute("SELECT * FROM beyblades WHERE id=?", (beyblade_id,)).fetchone()
    conn.close()
    return _row_to_beyblade(row) if row else None


def _row_to_beyblade(row: sqlite3.Row) -> Beyblade:
    return Beyblade(
        id=row["id"],
        bb_number=row["bb_number"],
        name=row["name"],
        era=row["era"],
        series=row["series"],
        release_type=row["release_type"],
        variant_note=row["variant_note"],
        bey_type=row["bey_type"],
        spin_direction=row["spin_direction"],
        release_date=row["release_date"],
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
    rows = conn.execute("""
        SELECT c.id, c.beyblade_id, c.quantity,
               b.bb_number, b.name, b.era, b.series, b.bey_type,
               b.spin_direction, b.face_bolt, b.energy_ring,
               b.fusion_wheel, b.spin_track, b.performance_tip
        FROM collection c
        JOIN beyblades b ON b.id = c.beyblade_id
        ORDER BY b.bb_number, b.name
    """).fetchall()
    conn.close()
    return [_row_to_entry(r) for r in rows]


def _row_to_entry(row: sqlite3.Row) -> CollectionEntry:
    return CollectionEntry(
        id=row["id"],
        beyblade_id=row["beyblade_id"],
        quantity=row["quantity"],
        bb_number=row["bb_number"],
        name=row["name"],
        era=row["era"],
        series=row["series"],
        bey_type=row["bey_type"],
        spin_direction=row["spin_direction"],
        face_bolt=row["face_bolt"],
        energy_ring=row["energy_ring"],
        fusion_wheel=row["fusion_wheel"],
        spin_track=row["spin_track"],
        performance_tip=row["performance_tip"],
    )


def is_in_collection(beyblade_id: int) -> Optional[int]:
    conn = _connect()
    row = conn.execute(
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
    total = cur.execute(
        "SELECT COALESCE(SUM(quantity),0) FROM collection"
    ).fetchone()[0]
    rows = cur.execute("""
        SELECT b.bey_type, COALESCE(SUM(c.quantity),0)
        FROM collection c
        JOIN beyblades b ON b.id = c.beyblade_id
        GROUP BY b.bey_type
    """).fetchall()
    conn.close()
    by_type = {r[0]: r[1] for r in rows}
    return {
        "total":   total,
        "attack":  by_type.get("Attack",  0),
        "defense": by_type.get("Defense", 0),
        "stamina": by_type.get("Stamina", 0),
        "balance": by_type.get("Balance", 0),
    }


# ── Random Booster queries ────────────────────────────────────────────────────

def get_random_boosters() -> list:
    conn = _connect()
    boosters = conn.execute(
        "SELECT * FROM random_boosters ORDER BY bb_number"
    ).fetchall()
    result = []
    for b in boosters:
        contents = conn.execute(
            "SELECT possible_bey, is_rare FROM random_booster_contents WHERE booster_id=?",
            (b["id"],),
        ).fetchall()
        result.append({
            "id":        b["id"],
            "bb_number": b["bb_number"],
            "name":      b["name"],
            "era":       b["era"],
            "contents":  [{"possible_bey": c["possible_bey"], "is_rare": c["is_rare"]}
                          for c in contents],
        })
    conn.close()
    return result


# ── Filter option lists ───────────────────────────────────────────────────────

ERA_OPTIONS    = ["All", "Pre-Hybrid", "Hybrid", "4D", "Zero-G"]
SERIES_OPTIONS = ["All", "Metal Fusion", "Metal Masters", "Metal Fury", "Shogun Steel"]
TYPE_OPTIONS   = ["All", "Attack", "Defense", "Stamina", "Balance"]
SPIN_OPTIONS   = ["All", "Right", "Left", "Both"]
