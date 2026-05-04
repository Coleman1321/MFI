from dataclasses import dataclass
from typing import Optional


@dataclass
class CollectionEntry:
    id: Optional[int]
    beyblade_id: int
    quantity: int
    # Joined beyblade fields
    bb_number: str = ""
    name: str = ""
    era: str = ""
    series: str = ""
    bey_type: str = ""
    spin_direction: str = "Right"
    face_bolt: str = ""
    energy_ring: str = ""
    fusion_wheel: str = ""
    spin_track: str = ""
    performance_tip: str = ""
