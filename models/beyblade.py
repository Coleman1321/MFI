from dataclasses import dataclass
from typing import Optional


@dataclass
class Beyblade:
    id: Optional[int]
    bb_number: str
    name: str
    era: str
    series: str
    release_type: str
    variant_note: str
    bey_type: str
    spin_direction: str
    release_date: Optional[str]
    face_bolt: str
    energy_ring: str
    fusion_wheel: str
    spin_track: str
    performance_tip: str
    image_path: Optional[str] = None

    @property
    def display_name(self) -> str:
        """Name with variant note appended when present."""
        if self.variant_note:
            return f"{self.name}  [{self.variant_note}]"
        return self.name

    @property
    def parts_summary(self) -> str:
        return (
            f"Face Bolt: {self.face_bolt}\n"
            f"Energy Ring: {self.energy_ring}\n"
            f"Fusion Wheel: {self.fusion_wheel}\n"
            f"Spin Track: {self.spin_track}\n"
            f"Performance Tip: {self.performance_tip}"
        )
