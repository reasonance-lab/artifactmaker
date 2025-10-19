"""Streamlit page for deleting saved class entries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional, Tuple

import streamlit as st

from app.constants import CLASS_BY_NAME, CLASS_OPTIONS
from app.gallery import MEDIA_EMOJIS
from app.storage import delete_entry, load_gallery
from app.styling import format_entry_time, inject_base_css


@dataclass
class EntryOption:
    label: str
    date_value: date
    entry_id: str
    created_at: datetime
    manual_text: Optional[str]
    transcript_text: Optional[str]
    media_counts: Tuple[Tuple[str, int], ...]


def _build_entry_options(class_slug: str) -> List[EntryOption]:
    options: List[EntryOption] = []
    for bucket in load_gallery(class_slug):
        for entry in bucket.entries:
            snippet_source = entry.text.manual_text or entry.text.transcript_text
            snippet: Optional[str] = None
            if snippet_source:
                snippet = snippet_source.strip()
                if len(snippet) > 70:
                    snippet = snippet[:67].strip() + "…"

            counts: List[Tuple[str, int]] = []
            for media_type, paths in entry.media_files.items():
                if paths:
                    counts.append((media_type, len(paths)))

            label_parts: List[str] = [
                bucket.date_value.strftime("%b %d, %Y"),
                format_entry_time(entry.created_at),
            ]
            if counts:
                readable = ", ".join(
                    f"{count} {media_type}{'s' if count > 1 else ''}"
                    for media_type, count in counts
                )
                label_parts.append(readable)
            if snippet:
                label_parts.append(f'"{snippet}"')

            options.append(
                EntryOption(
                    label=" · ".join(label_parts),
                    date_value=bucket.date_value,
                    entry_id=entry.entry_id,
                    created_at=entry.created_at,
                    manual_text=entry.text.manual_text,
                    transcript_text=entry.text.transcript_text,
                    media_counts=tuple(counts),
                )
            )
    return options


def _render_entry_details(selected_option: EntryOption) -> None:
    st.markdown(
        f"<div class='entry-meta'>Captured on {selected_option.date_value.strftime('%A, %B %d, %Y')} at {format_entry_time(selected_option.created_at)}</div>",
        unsafe_allow_html=True,
    )

    if selected_option.media_counts:
        items = []
        for media_type, count in selected_option.media_counts:
            emoji = MEDIA_EMOJIS.get(media_type, "•")
            label = f"{count} {media_type}{'s' if count > 1 else ''}"
            items.append(f"<li>{emoji} {label}</li>")
        st.markdown(
            f"<ul style='padding-left:1.1rem;margin-top:0.45rem;margin-bottom:0.9rem;'>{''.join(items)}</ul>",
            unsafe_allow_html=True,
        )
    else:
        st.caption("No media files were attached to this entry.")

    if selected_option.manual_text:
        st.markdown("**Typed notes**")
        st.markdown(
            f"<div class='entry-text'>{selected_option.manual_text}</div>",
            unsafe_allow_html=True,
        )
    if selected_option.transcript_text:
        st.markdown("**Voice transcript**")
        st.markdown(
            f"<div class='entry-text'>{selected_option.transcript_text}</div>",
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(
        page_title="Manage entries",
        page_icon="🗑️",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    inject_base_css()

    feedback = st.session_state.pop("delete_feedback", None)
    if feedback:
        status, message = feedback
        if status == "success":
            st.success(message)
        elif status == "warning":
            st.warning(message)
        else:
            st.error(message)

    st.markdown("<div class='app-title'>Manage saved entries</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='app-subtitle'>Remove outdated uploads when a class no longer needs them.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='field-label'>Class</div>", unsafe_allow_html=True)
    class_name = st.selectbox(
        "Choose class",
        CLASS_OPTIONS,
        key="delete_class_select",
        label_visibility="collapsed",
    )
    class_info = CLASS_BY_NAME[class_name]

    options = _build_entry_options(class_info.slug)
    if not options:
        st.markdown(
            "<div class='empty-state'>No entries to delete for this class yet.</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown("<div class='field-label' style='margin-top:1.2rem;'>Entry</div>", unsafe_allow_html=True)
    selected_option = st.selectbox(
        "Select an entry to delete",
        options,
        format_func=lambda option: option.label,
        key="entry_delete_selector",
        label_visibility="collapsed",
    )

    st.markdown("<div class='media-pill'>Entry summary</div>", unsafe_allow_html=True)
    _render_entry_details(selected_option)

    with st.container():
        st.markdown("<div class='danger-zone'>", unsafe_allow_html=True)
        st.markdown("<h3>Delete entry</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p>This permanently removes the media, transcripts, and notes stored for this entry.</p>",
            unsafe_allow_html=True,
        )
        if st.button("Delete selected entry", key="confirm_delete", use_container_width=True):
            if delete_entry(class_info.slug, selected_option.date_value, selected_option.entry_id):
                st.session_state["delete_feedback"] = (
                    "success",
                    f"Deleted entry from {selected_option.date_value.isoformat()} in {class_info.name}.",
                )
                st.rerun()
            else:
                st.session_state["delete_feedback"] = (
                    "error",
                    "We couldn't delete that entry. It may have already been removed.",
                )
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
