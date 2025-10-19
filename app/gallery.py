"""Rendering helpers for gallery pages."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import streamlit as st

from .constants import CLASS_BY_SLUG, ClassInfo
from .storage import load_gallery
from .styling import format_entry_time, inject_base_css


MEDIA_EMOJIS = {"image": "🖼️", "video": "🎬", "audio": "🔊"}


def _render_media_grid(paths: Iterable[Path], media_type: str) -> None:
    if not paths:
        return
    if media_type == "image":
        images = [str(path) for path in paths]
        st.image(images, use_column_width=True)
        return
    for path in paths:
        if media_type == "video":
            st.video(str(path))
        elif media_type == "audio":
            st.audio(str(path))


def _render_entry_card(entry) -> None:
    with st.container():
        st.markdown("<div class='entry-card'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='entry-meta'>{format_entry_time(entry.created_at)}</div>",
            unsafe_allow_html=True,
        )

        if entry.text.manual_text:
            st.markdown("**Typed notes**")
            st.markdown(
                f"<div class='entry-text'>{entry.text.manual_text}</div>",
                unsafe_allow_html=True,
            )
        if entry.text.transcript_text:
            st.markdown("**Voice transcript**")
            st.markdown(
                f"<div class='entry-text'>{entry.text.transcript_text}</div>",
                unsafe_allow_html=True,
            )
        if entry.media_files.get("audio") and not entry.text.transcript_text:
            st.caption("Voice transcript unavailable for this clip.")

        for media_type in ("image", "video", "audio"):
            paths = entry.media_files.get(media_type, [])
            if not paths:
                continue
            emoji = MEDIA_EMOJIS.get(media_type, "")
            st.markdown(f"<div class='media-pill'>{emoji} {media_type.title()}</div>", unsafe_allow_html=True)
            _render_media_grid(paths, media_type)
        st.markdown("</div>", unsafe_allow_html=True)


def render_gallery_page(class_slug: str) -> None:
    class_info: ClassInfo = CLASS_BY_SLUG[class_slug]
    st.set_page_config(
        page_title=class_info.gallery_title,
        page_icon="🗂️",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    inject_base_css()

    st.markdown(
        f"<div class='app-title'>{class_info.gallery_title}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='app-subtitle'>Browse saved media grouped by date.</div>",
        unsafe_allow_html=True,
    )

    buckets = load_gallery(class_slug)
    if not buckets:
        st.info("No entries have been saved yet. Capture something from the recorder page to get started.")
        return

    for bucket in buckets:
        st.markdown(
            f"<div class='gallery-date'><span>{bucket.date_value.strftime('%A, %B %d, %Y')}</span></div>",
            unsafe_allow_html=True,
        )
        for entry in bucket.entries:
            _render_entry_card(entry)
