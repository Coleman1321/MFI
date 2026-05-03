from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Beyblade:
    id: Optional[int]
    name: str
    series: str
    bey_type: str
    face_bolt: str
    energy_ring: str
    fusion_wheel: str
    spin_track: str
    performance_tip: str
    image_path: Optional[str] = None

    @property
    def parts_summary(self) -> str:
        return (
            f"Face Bolt: {self.face_bolt}\n"
            f"Energy Ring: {self.energy_ring}\n"
            f"Fusion Wheel: {self.fusion_wheel}\n"
            f"Spin Track: {self.spin_track}\n"
            f"Performance Tip: {self.performance_tip}"
        )
