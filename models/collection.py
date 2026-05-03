from dataclasses import dataclass
from typing import Optional


@dataclass
class CollectionEntry:
    id: Optional[int]
    beyblade_id: int
    quantity: int
    name: str = ""
    series: str = ""
    bey_type: str = ""
    face_bolt: str = ""
    energy_ring: str = ""
    fusion_wheel: str = ""
    spin_track: str = ""
    performance_tip: str = ""
