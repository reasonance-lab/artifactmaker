"""Persistence helpers for the Streamlit classroom recorder app."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from uuid import uuid4

import shutil

from slugify import slugify

from .constants import CLASS_BY_NAME, CLASS_BY_SLUG, ClassInfo


DATA_ROOT = Path(os.environ.get("DATA_ROOT", "data"))
MEDIA_EXTENSIONS = {
    "image": {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".heic"},
    "video": {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"},
    "audio": {".wav", ".mp3", ".m4a", ".aac", ".ogg"},
}
TEXT_FILES = {"notes.txt", "voice_transcript.txt"}

@dataclass
class EntryText:
    manual_text: Optional[str] = None
    transcript_text: Optional[str] = None


@dataclass
class EntryContent:
    """Represents a single saved entry in the gallery."""

    entry_id: str
    created_at: datetime
    media_files: Dict[str, List[Path]]
    text: EntryText
    directory: Path


@dataclass
class DateBucket:
    date_value: date
    entries: List[EntryContent]


def _safe_filename(original_name: str) -> str:
    stem = slugify(Path(original_name).stem, lowercase=False) or "file"
    suffix = Path(original_name).suffix.lower()
    return f"{stem}{suffix}"


def ensure_entry_dir(class_name: str, day: date) -> Path:
    """Create and return a directory for a new entry."""

    class_info = CLASS_BY_NAME[class_name]
    date_dir = DATA_ROOT / class_info.slug / day.isoformat()
    entry_id = f"{datetime.now().strftime('%H%M%S')}-{uuid4().hex[:8]}"
    entry_dir = date_dir / entry_id
    entry_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "class": class_info.slug,
        "date": day.isoformat(),
        "entry_id": entry_id,
        "created_at": datetime.now().isoformat(),
    }
    (entry_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return entry_dir


def save_uploaded_files(entry_dir: Path, uploaded_files: Iterable) -> List[Path]:
    saved_paths: List[Path] = []
    timestamp_prefix = datetime.now().strftime("%H%M%S")
    for position, file in enumerate(uploaded_files):
        if not file:
            continue
        filename = _safe_filename(file.name)
        unique_name = f"{timestamp_prefix}-{position:02d}-{filename}"
        destination = entry_dir / unique_name
        with destination.open("wb") as output:
            output.write(file.getbuffer())
        saved_paths.append(destination)
    return saved_paths


def save_audio(entry_dir: Path, audio_bytes: bytes, suffix: str = ".wav") -> Path:
    filename = f"audio-{datetime.now().strftime('%H%M%S')}{suffix}"
    destination = entry_dir / filename
    with destination.open("wb") as output:
        output.write(audio_bytes)
    return destination


def save_text(entry_dir: Path, name: str, content: str) -> Path:
    destination = entry_dir / name
    destination.write_text(content.strip() + "\n", encoding="utf-8")
    return destination


def load_gallery(class_slug: str) -> List[DateBucket]:
    class_info: ClassInfo = CLASS_BY_SLUG[class_slug]
    class_dir = DATA_ROOT / class_info.slug
    if not class_dir.exists():
        return []

    buckets: List[DateBucket] = []
    for date_dir in sorted(class_dir.iterdir(), reverse=True):
        if not date_dir.is_dir():
            continue
        try:
            bucket_date = date.fromisoformat(date_dir.name)
        except ValueError:
            continue
        entries: List[EntryContent] = []
        for entry_dir in sorted(date_dir.iterdir(), reverse=True):
            if not entry_dir.is_dir():
                continue
            metadata_path = entry_dir / "metadata.json"
            created_at = datetime.fromtimestamp(entry_dir.stat().st_mtime)
            if metadata_path.exists():
                try:
                    metadata = json.loads(metadata_path.read_text())
                    created_raw = metadata.get("created_at")
                    if created_raw:
                        created_at = datetime.fromisoformat(created_raw)
                except (json.JSONDecodeError, ValueError):
                    pass
            media: Dict[str, List[Path]] = {"image": [], "video": [], "audio": []}
            text = EntryText()
            for path in sorted(entry_dir.iterdir()):
                if path.name in TEXT_FILES:
                    content = path.read_text(encoding="utf-8").strip()
                    if path.name == "notes.txt":
                        text.manual_text = content
                    elif path.name == "voice_transcript.txt":
                        text.transcript_text = content
                    continue
                suffix = path.suffix.lower()
                for media_type, extensions in MEDIA_EXTENSIONS.items():
                    if suffix in extensions:
                        media[media_type].append(path)
                        break
            entries.append(
                EntryContent(
                    entry_id=entry_dir.name,
                    created_at=created_at,
                    media_files=media,
                    text=text,
                    directory=entry_dir,
                )
            )
        if entries:
            buckets.append(DateBucket(date_value=bucket_date, entries=entries))
    return buckets


def delete_entry(class_slug: str, entry_date: date, entry_id: str) -> bool:
    """Delete a saved entry directory and clean up empty parents."""

    class_info: ClassInfo = CLASS_BY_SLUG[class_slug]
    entry_dir = DATA_ROOT / class_info.slug / entry_date.isoformat() / entry_id
    if not entry_dir.exists() or not entry_dir.is_dir():
        return False

    try:
        shutil.rmtree(entry_dir)
    except OSError:
        return False
    date_dir = entry_dir.parent
    try:
        if date_dir.exists() and not any(date_dir.iterdir()):
            date_dir.rmdir()
    except OSError:
        pass

    class_dir = DATA_ROOT / class_info.slug
    try:
        if class_dir.exists() and not any(class_dir.iterdir()):
            class_dir.rmdir()
    except OSError:
        pass

    return True
