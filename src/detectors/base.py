from __future__ import annotations

from typing import Protocol

from src.core.models import DetectorSignal


class Detector(Protocol):
    name: str
    weight: float

    def detect(self, text: str) -> DetectorSignal:
        ...
