"""Shared constants for the Streamlit classroom recorder app."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ClassInfo:
    """Metadata about a single class option in the app."""

    name: str
    slug: str
    gallery_title: str
    accent_color: str


CLASS_INFOS: List[ClassInfo] = [
    ClassInfo(
        name="AP Chemistry",
        slug="ap-chemistry",
        gallery_title="AP Chemistry Gallery",
        accent_color="#2563eb",
    ),
    ClassInfo(
        name="Chemistry",
        slug="chemistry",
        gallery_title="Chemistry Gallery",
        accent_color="#059669",
    ),
    ClassInfo(
        name="PLTW Medical Interventions",
        slug="pltw-medical-interventions",
        gallery_title="PLTW Medical Interventions Gallery",
        accent_color="#d97706",
    ),
]

CLASS_OPTIONS: List[str] = [info.name for info in CLASS_INFOS]
CLASS_BY_NAME: Dict[str, ClassInfo] = {info.name: info for info in CLASS_INFOS}
CLASS_BY_SLUG: Dict[str, ClassInfo] = {info.slug: info for info in CLASS_INFOS}
