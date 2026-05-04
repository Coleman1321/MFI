"""
Seed data for the MFB index.

Each BEYBLADES entry is a dict with keys matching the beyblades table columns.
Tuple layout for _b() helper:
  bb_number, name, era, series, release_type, variant_note,
  bey_type, spin_direction, release_date,
  face_bolt, energy_ring, fusion_wheel, spin_track, performance_tip
"""

# ── Era / series constants ────────────────────────────────────────────────────
PH = "Pre-Hybrid"
HY = "Hybrid"
FD = "4D"
ZG = "Zero-G"

MF  = "Metal Fusion"
MM  = "Metal Masters"
MFU = "Metal Fury"
SS  = "Shogun Steel"

ST  = "Starter"
BO  = "Booster"
RB  = "Random Booster"
SE  = "Set Exclusive"
PR  = "Prize"
LE  = "Limited Edition"

R   = "Right"
L   = "Left"
BO2 = "Both"


def _b(bb, name, era, series, rtype, variant, btype, spin, date,
       fb, er, fw, track, tip):
    return {
        "bb_number":      bb,
        "name":           name,
        "era":            era,
        "series":         series,
        "release_type":   rtype,
        "variant_note":   variant,
        "bey_type":       btype,
        "spin_direction": spin,
        "release_date":   date,
        "face_bolt":      fb,
        "energy_ring":    er,
        "fusion_wheel":   fw,
        "spin_track":     track,
        "performance_tip": tip,
    }


# ── Pre-Hybrid (Metal System) — BB-00 to BB-26 ───────────────────────────────
# Metal System: Face Bolt + Energy Ring (Clear Wheel) + Metal Wheel + Track + Tip.
# fusion_wheel = the Metal Wheel, which shares a name with the bey for pre-Hybrid.

BEYBLADES = [
    _b("BB-00",  "Pegasis Prototype",        PH, MF,  PR,  "",  "Attack",  R, None,
       "Pegasis",    "Pegasis",    "Pegasis",    "105",   "F"),
    _b("BB-01",  "Pegasis 105F",             PH, MF,  ST,  "",  "Attack",  R, "2008-07-05",
       "Pegasis",    "Pegasis",    "Pegasis",    "105",   "F"),
    _b("BB-02",  "Bull 125SF",               PH, MF,  ST,  "",  "Balance", R, "2008-07-05",
       "Bull",       "Bull",       "Bull",       "125",   "SF"),
    _b("BB-03",  "Sagittario 145S",          PH, MF,  ST,  "",  "Stamina", R, "2008-07-05",
       "Sagittario", "Sagittario", "Sagittario", "145",   "S"),
    _b("BB-04",  "Leone 145D",               PH, MF,  ST,  "",  "Defense", R, "2008-07-05",
       "Leone",      "Leone",      "Leone",      "145",   "D"),
    _b("BB-05",  "Pegasis 145D",             PH, MF,  BO,  "",  "Balance", R, "2008-07-05",
       "Pegasis",    "Pegasis",    "Pegasis",    "145",   "D"),
    _b("BB-06",  "Bull 145S",                PH, MF,  BO,  "",  "Stamina", R, "2008-07-05",
       "Bull",       "Bull",       "Bull",       "145",   "S"),
    _b("BB-07",  "Sagittario 125SF",         PH, MF,  BO,  "",  "Balance", R, "2008-07-05",
       "Sagittario", "Sagittario", "Sagittario", "125",   "SF"),
    _b("BB-08",  "Leone 105F",               PH, MF,  BO,  "",  "Attack",  R, "2008-07-05",
       "Leone",      "Leone",      "Leone",      "105",   "F"),
    _b("BB-11",  "Wolf D125B",               PH, MF,  ST,  "",  "Defense", R, "2008-09-13",
       "Wolf",       "Wolf",       "Wolf",       "D125",  "B"),
    _b("BB-12",  "Wolf 105F",                PH, MF,  BO,  "",  "Attack",  R, "2008-09-13",
       "Wolf",       "Wolf",       "Wolf",       "105",   "F"),
    _b("BB-18",  "Libra DF145BS",            PH, MF,  ST,  "",  "Stamina", R, "2008-12-13",
       "Libra",      "Libra",      "Libra",      "DF145", "BS"),
    _b("BB-22",  "Virgo DF145BS",            PH, MF,  BO,  "",  "Stamina", R, "2009-03-28",
       "Virgo",      "Virgo",      "Virgo",      "DF145", "BS"),
    _b("BB-23",  "L-Drago 105F",             PH, MF,  ST,  "",  "Attack",  L, "2009-03-28",
       "L-Drago",    "L-Drago I",  "L-Drago",    "105",   "F"),
    _b("BB-24",  "Escolpio WD145B",          PH, MF,  BO,  "",  "Defense", R, "2009-03-28",
       "Escolpio",   "Escolpio",   "Escolpio",   "WD145", "B"),
    _b("BB-26",  "Gemios DF145FS",           PH, MF,  BO,  "",  "Balance", R, "2009-05-30",
       "Gemios",     "Gemios",     "Gemios",     "DF145", "FS"),
    # Pre-Hybrid wheels re-issued in later Random Boosters (Metal Masters window)
    _b("BB-72",  "Aquario 105F",             PH, MM,  RB,  "Random Booster Light Vol. 2", "Attack",  R, None,
       "Aquario",    "Aquario",    "Aquario",    "105",   "F"),
    _b("BB-83",  "Pisces DF145BS",           PH, MM,  RB,  "Random Booster Vol. 5",       "Stamina", R, None,
       "Pisces",     "Pisces",     "Pisces",     "DF145", "BS"),
    _b("BB-89",  "Aries 145D",               PH, MM,  BO,  "",  "Defense", R, None,
       "Aries",      "Aries",      "Aries",      "145",   "D"),

    # ── Hybrid Wheel System — Metal Fusion era ────────────────────────────────
    _b("BB-27",  "Capricorne 100HF",         HY, MF,  BO,  "",  "Attack",  R, "2009-05-30",
       "Capricorne", "Capricorne", "Capricorne", "100",   "HF"),
    _b("BB-28",  "Storm Pegasis 105RF",      HY, MF,  ST,  "",  "Attack",  R, "2009-05-30",
       "Pegasis",    "Pegasis I",  "Storm",      "105",   "RF"),
    _b("BB-28A", "Storm Pegasis 105RF",      HY, MF,  SE,  "Clear ver. — Random Booster Light Vol. 2", "Attack", R, None,
       "Pegasis",    "Pegasis I",  "Storm",      "105",   "RF"),
    _b("BB-29",  "Dark Wolf DF145FS",        HY, MF,  BO,  "",  "Balance", R, "2009-05-30",
       "Wolf",       "Wolf",       "Dark",       "DF145", "FS"),
    _b("BB-30",  "Rock Leone 145WB",         HY, MF,  ST,  "",  "Defense", R, "2009-07-18",
       "Leone",      "Leone",      "Rock",       "145",   "WB"),
    _b("BB-35",  "Flame Sagittario C145S",   HY, MF,  ST,  "",  "Stamina", R, "2009-08-08",
       "Sagittario", "Sagittario I","Flame",     "C145",  "S"),
    _b("BB-40",  "Dark Bull H145SD",         HY, MF,  ST,  "",  "Stamina", R, "2009-09-12",
       "Bull",       "Bull",       "Dark",       "H145",  "SD"),
    _b("BB-43",  "Lightning L-Drago 100HF",  HY, MF,  ST,  "",  "Attack",  L, "2009-09-12",
       "L-Drago",    "L-Drago I",  "Lightning",  "100",   "HF"),
    _b("BB-47",  "Earth Aquila 145WD",       HY, MF,  BO,  "",  "Stamina", R, "2009-10-10",
       "Aquila",     "Aquila",     "Earth",      "145",   "WD"),
    _b("BB-48",  "Flame Libra T125ES",       HY, MF,  ST,  "",  "Stamina", R, "2009-10-10",
       "Libra",      "Libra",      "Flame",      "T125",  "ES"),
    _b("BB-50",  "Storm Capricorne M145Q",   HY, MF,  BO,  "",  "Attack",  R, "2009-10-10",
       "Capricorne", "Capricorne", "Storm",      "M145",  "Q"),
    _b("BB-55",  "Dark Cancer CH120SF",      HY, MF,  BO,  "",  "Balance", R, "2009-12-19",
       "Cancer",     "Cancer",     "Dark",       "CH120", "SF"),
    _b("BB-59",  "Burn Phoenix 135MS",       HY, MF,  ST,  "",  "Stamina", R, "2010-01-30",
       "Phoenix",    "Phoenix",    "Burn",       "135",   "MS"),
    _b("BB-65",  "Rock Escolpio T125JB",     HY, MF,  BO,  "",  "Defense", R, "2010-03-06",
       "Escolpio",   "Escolpio",   "Rock",       "T125",  "JB"),
    _b("BB-69",  "Poison Serpent SW145SD",   HY, MF,  BO,  "",  "Stamina", R, "2010-04-24",
       "Serpent",    "Serpent",    "Poison",     "SW145", "SD"),

    # ── Hybrid Wheel System — Metal Masters era ───────────────────────────────
    _b("BB-70",  "Galaxy Pegasis W105R²F",   HY, MM,  ST,  "",  "Attack",  R, "2010-04-24",
       "Pegasis",    "Pegasis II", "Galaxy",     "W105",  "R²F"),
    _b("BB-70A", "Galaxy Pegasis W105R²F",   HY, MM,  SE,  "Clear orange — Beyblade Metal Masters Set", "Attack", R, None,
       "Pegasis",    "Pegasis II", "Galaxy",     "W105",  "R²F"),
    _b("BB-71",  "Ray Unicorno D125CS",      HY, MM,  ST,  "",  "Balance", R, "2010-04-24",
       "Unicorno",   "Unicorno I", "Ray",        "D125",  "CS"),
    _b("BB-74",  "Thermal Lacerta WA130HF",  HY, MM,  BO,  "",  "Attack",  R, "2010-06-19",
       "Lacerta",    "Lacerta",    "Thermal",    "WA130", "HF"),
    _b("BB-78",  "Rock Giraffe R145WB",      HY, MM,  BO,  "",  "Defense", R, "2010-07-17",
       "Giraffe",    "Giraffe",    "Rock",       "R145",  "WB"),
    _b("BB-80",  "Gravity Perseus AD145WD",  HY, MM,  ST,  "",  "Balance", BO2,"2010-08-07",
       "Perseus",    "Perseus",    "Gravity",    "AD145", "WD"),
    _b("BB-80A", "Gravity Perseus AD145WD",  HY, MM,  RB,  "Dark purple ver. — Random Booster Vol. 7", "Balance", BO2, None,
       "Perseus",    "Perseus",    "Gravity",    "AD145", "WD"),
    _b("BB-88",  "Meteo L-Drago LW105LF",    HY, MM,  ST,  "",  "Attack",  L, "2010-10-16",
       "L-Drago",    "L-Drago II", "Meteo",      "LW105", "LF"),
    _b("BB-91",  "Ray Gil 100RSF",           HY, MM,  ST,  "",  "Attack",  R, "2010-11-20",
       "Gil",        "Gil",        "Ray",        "100",   "RSF"),
    _b("BB-95",  "Flame Byxis 230WD",        HY, MM,  ST,  "",  "Stamina", R, "2011-01-15",
       "Byxis",      "Byxis",      "Flame",      "230",   "WD"),
    _b("BB-99",  "Hell Kerbecs BD145DS",     HY, MM,  ST,  "",  "Stamina", R, "2011-03-19",
       "Kerbecs",    "Kerbecs",    "Hell",       "BD145", "DS"),
    _b("BB-99A", "Hell Kerbecs BD145DS",     HY, MM,  RB,  "Gold ver. — Random Booster Vol. 9", "Stamina", R, None,
       "Kerbecs",    "Kerbecs",    "Hell",       "BD145", "DS"),
    _b("BB-102", "Screw Capricorne 90MF",    HY, MM,  BO,  "",  "Attack",  R, "2011-04-16",
       "Capricorne", "Capricorne", "Screw",      "90",    "MF"),

    # ── 4D System — Metal Fury era ────────────────────────────────────────────
    # 4D Wheels have a PC Frame + Inner; combined track/tip notation used where applicable.
    _b("BB-104", "Basalt Horogium 145WD",    FD, MFU, ST,  "",  "Defense", R, "2011-06-18",
       "Horogium",   "Horogium",   "Basalt",     "145",          "WD"),
    _b("BB-104A","Basalt Horogium 145WD",    FD, MFU, RB,  "Black ver. — Random Booster Vol. 9", "Defense", R, None,
       "Horogium",   "Horogium",   "Basalt",     "145",          "WD"),
    _b("BB-105", "Big Bang Pegasis F:D",     FD, MFU, ST,  "",  "Attack",  R, "2011-07-16",
       "Pegasis",    "Pegasis III","Big Bang",   "F:D (4D System)","F:D"),
    _b("BB-106", "Fang Leone 130W²D",        FD, MFU, ST,  "",  "Defense", R, "2011-08-06",
       "Leone",      "Leone",      "Fang",       "130",          "W²D"),
    _b("BB-108", "L-Drago Destroy F:S",      FD, MFU, ST,  "",  "Attack",  L, "2011-08-06",
       "L-Drago",    "L-Drago III","L-Drago Destroy","F:S (4D System)","F:S"),
    _b("BB-113", "Scythe Kronos T125EDS",    FD, MFU, BO,  "",  "Stamina", R, "2011-10-15",
       "Kronos",     "Kronos",     "Scythe",     "T125",         "EDS"),
    _b("BB-114", "VariAres D:D",             FD, MFU, ST,  "",  "Attack",  BO2,"2011-11-19",
       "Aries",      "Aries II",   "VariAres",   "D:D (4D System)","D:D"),
    _b("BB-118", "Phantom Orion B:D",        FD, MFU, BO,  "",  "Stamina", R, "2012-01-21",
       "Orion",      "Orion",      "Phantom",    "B:D (4D System)","B:D"),
    _b("BB-119", "Death Quetzalcoatl 125RDF",FD, MFU, BO,  "",  "Stamina", R, "2012-01-21",
       "Quetzalcoatl","Quetzalcoatl II","Death", "125",          "RDF"),
    _b("BB-122", "Diablo Nemesis X:D",       FD, MFU, ST,  "",  "Balance", R, "2012-03-17",
       "Nemesis",    "Nemesis",    "Diablo",     "X:D (4D System)","X:D"),
    _b("BB-124", "Kreis Cygnus 145WD",       FD, MFU, BO,  "",  "Stamina", R, "2012-04-14",
       "Cygnus",     "Cygnus",     "Kreis",      "145",          "WD"),
    _b("BB-126", "Flash Sagittario 230WD",   FD, MFU, BO,  "",  "Stamina", R, "2012-05-12",
       "Sagittario", "Sagittario II","Flash",    "230",          "WD"),

    # ── Zero-G / Shogun Steel — BBG series ───────────────────────────────────
    # Zero-G uses Chrome Wheel (metal) + Crystal Wheel (plastic) on a round Zero-G stadium.
    # Mapped to: face_bolt=Stone Face, energy_ring=Crystal Wheel, fusion_wheel=Chrome Wheel.
    _b("BBG-01", "Samurai Ifraid W145CF",    ZG, SS,  ST,  "",  "Attack",  R, "2012-04-28",
       "Stone Face", "Samurai",    "Ifraid",     "W145",  "CF"),
    _b("BBG-02", "Shinobi Saramanda SW145SD",ZG, SS,  ST,  "",  "Defense", R, "2012-04-28",
       "Stone Face", "Shinobi",    "Saramanda",  "SW145", "SD"),
    _b("BBG-08", "Pirates Orojya 145D",      ZG, SS,  BO,  "",  "Defense", R, "2012-07-14",
       "Stone Face", "Pirates",    "Orojya",     "145",   "D"),
    _b("BBG-10", "Guardian Revizer 160SB",   ZG, SS,  ST,  "",  "Defense", R, "2012-08-11",
       "Stone Face", "Guardian",   "Revizer",    "160",   "SB"),
    _b("BBG-12", "Archer Gryph C145S",       ZG, SS,  BO,  "",  "Balance", R, "2012-09-15",
       "Stone Face", "Archer",     "Gryph",      "C145",  "S"),
    _b("BBG-16", "Dark Knight Dragooon LW160BSF", ZG, SS, BO, "", "Attack", R, "2012-11-10",
       "Stone Face", "Dark Knight","Dragooon",   "LW160", "BSF"),
]


# ── Random Booster catalogue ──────────────────────────────────────────────────
# Each entry: booster bb_number, display name, era, and the possible beys (by name).
# is_rare=1 marks short-print / chase pulls.

RANDOM_BOOSTERS = [
    {
        "bb_number": "BB-33",
        "name":      "Random Booster Light Vol. 1",
        "era":       PH,
        "contents":  [
            {"possible_bey": "Pegasis 105F",       "is_rare": 0},
            {"possible_bey": "Bull 125SF",          "is_rare": 0},
            {"possible_bey": "Sagittario 145S",     "is_rare": 0},
            {"possible_bey": "Leone 145D",          "is_rare": 0},
            {"possible_bey": "Wolf D125B",          "is_rare": 0},
            {"possible_bey": "L-Drago 105F",        "is_rare": 1},
            {"possible_bey": "Libra DF145BS",       "is_rare": 1},
        ],
    },
    {
        "bb_number": "BB-46",
        "name":      "Random Booster Vol. 1 Heavy Metal Ver.",
        "era":       HY,
        "contents":  [
            {"possible_bey": "Storm Pegasis 105RF", "is_rare": 0},
            {"possible_bey": "Rock Leone 145WB",    "is_rare": 0},
            {"possible_bey": "Dark Wolf DF145FS",   "is_rare": 0},
            {"possible_bey": "Flame Sagittario C145S", "is_rare": 0},
            {"possible_bey": "Dark Bull H145SD",    "is_rare": 0},
            {"possible_bey": "Lightning L-Drago 100HF", "is_rare": 1},
        ],
    },
    {
        "bb_number": "BB-56",
        "name":      "Random Booster Vol. 3",
        "era":       HY,
        "contents":  [
            {"possible_bey": "Earth Aquila 145WD",  "is_rare": 0},
            {"possible_bey": "Flame Libra T125ES",  "is_rare": 0},
            {"possible_bey": "Storm Capricorne M145Q", "is_rare": 0},
            {"possible_bey": "Dark Cancer CH120SF", "is_rare": 0},
            {"possible_bey": "Burn Phoenix 135MS",  "is_rare": 1},
        ],
    },
    {
        "bb_number": "BB-93",
        "name":      "Random Booster Vol. 8",
        "era":       HY,
        "contents":  [
            {"possible_bey": "Galaxy Pegasis W105R²F",  "is_rare": 0},
            {"possible_bey": "Ray Unicorno D125CS",     "is_rare": 0},
            {"possible_bey": "Thermal Lacerta WA130HF", "is_rare": 0},
            {"possible_bey": "Rock Giraffe R145WB",     "is_rare": 0},
            {"possible_bey": "Gravity Perseus AD145WD", "is_rare": 1},
            {"possible_bey": "Meteo L-Drago LW105LF",  "is_rare": 1},
        ],
    },
    {
        "bb_number": "BB-101",
        "name":      "Random Booster Vol. 10 Limited",
        "era":       FD,
        "contents":  [
            {"possible_bey": "Hell Kerbecs BD145DS",   "is_rare": 0},
            {"possible_bey": "Screw Capricorne 90MF",  "is_rare": 0},
            {"possible_bey": "Basalt Horogium 145WD",  "is_rare": 1},
            {"possible_bey": "Big Bang Pegasis F:D",   "is_rare": 1},
        ],
    },
]
