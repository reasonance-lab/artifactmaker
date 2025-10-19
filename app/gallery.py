"""Rendering helpers for gallery pages."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

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
        st.image(images, use_container_width=True)
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
            st.markdown(
                "<div class='entry-warning'>Voice transcript unavailable for this clip."
                " Ensure Whisper is installed and configured if you need automatic transcription.</div>",
                unsafe_allow_html=True,
            )

        for media_type in ("image", "video", "audio"):
            paths = entry.media_files.get(media_type, [])
            if not paths:
                continue
            emoji = MEDIA_EMOJIS.get(media_type, "")
            st.markdown(f"<div class='media-pill'>{emoji} {media_type.title()}</div>", unsafe_allow_html=True)
            _render_media_grid(paths, media_type)
        st.markdown("</div>", unsafe_allow_html=True)

def _build_slides(buckets) -> List[Tuple["DateBucket", "EntryContent"]]:
    slides: List[Tuple["DateBucket", "EntryContent"]] = []
    for bucket in buckets:
        for entry in bucket.entries:
            slides.append((bucket, entry))
    return slides


def render_gallery_page(class_slug: str) -> None:
    class_info: ClassInfo = CLASS_BY_SLUG[class_slug]
    st.set_page_config(
        page_title=class_info.gallery_title,
        page_icon="🗂️",
        layout="centered",
        initial_sidebar_state="expanded",
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
        st.markdown(
            "<div class='empty-state'>\n"
            "<strong>No entries yet.</strong> Once you save notes from the recorder, they'll appear here grouped by date with their media clips.\n"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    slides = _build_slides(buckets)
    if not slides:
        st.markdown(
            "<div class='empty-state'>\n"
            "<strong>No entries yet.</strong> Once you save notes from the recorder, they'll appear here grouped by date with their media clips.\n"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    index_key = f"{class_slug}_slide_index"
    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    total_slides = len(slides)
    st.session_state[index_key] = max(0, min(st.session_state[index_key], total_slides - 1))
    current_index = st.session_state[index_key]

    current_bucket, current_entry = slides[current_index]

    with st.container():
        st.markdown("<div class='gallery-slider'>", unsafe_allow_html=True)
        left_col, center_col, right_col = st.columns([1, 6, 1], gap="small")

        with left_col:
            st.markdown("<div class='slider-arrow left'>", unsafe_allow_html=True)
            disable_prev = current_index == 0 or total_slides == 1
            if st.button(
                "‹",
                key=f"{class_slug}-prev",
                disabled=disable_prev,
                help="Show a newer entry",
            ):
                st.session_state[index_key] = max(0, current_index - 1)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with center_col:
            st.markdown("<div class='gallery-slide'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='gallery-date'><span>{current_bucket.date_value.strftime('%A, %B %d, %Y')}</span></div>",
                unsafe_allow_html=True,
            )
            _render_entry_card(current_entry)
            st.markdown(
                f"<div class='slider-counter'>{current_index + 1} / {total_slides}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown("<div class='slider-arrow right'>", unsafe_allow_html=True)
            disable_next = current_index == (total_slides - 1) or total_slides == 1
            if st.button(
                "›",
                key=f"{class_slug}-next",
                disabled=disable_next,
                help="Show an earlier entry",
            ):
                st.session_state[index_key] = min(total_slides - 1, current_index + 1)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
