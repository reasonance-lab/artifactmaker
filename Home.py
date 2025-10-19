"""Streamlit entry point for the classroom media recorder."""

from __future__ import annotations

import datetime as dt
from typing import List, Optional

import streamlit as st
from audio_recorder_streamlit import audio_recorder

from app.constants import CLASS_BY_NAME, CLASS_OPTIONS
from app.storage import ensure_entry_dir, save_audio, save_text, save_uploaded_files
from app.styling import inject_base_css
from app.transcription import AudioState, transcribe_audio


def _render_header() -> None:
    st.markdown("<div class='app-title'>Classroom Capture</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='app-subtitle'>Quickly capture labs, experiments, and reflections in one place.</div>",
        unsafe_allow_html=True,
    )


def _render_recorder_controls() -> None:
    st.markdown("<div class='media-pill'>🎙️ Voice recorder</div>", unsafe_allow_html=True)
    record_col, clear_col = st.columns([4, 1])

    with record_col:
        audio_bytes = audio_recorder(
            text="Tap to record",
            recording_color="#ef4444",
            neutral_color="#0ea5e9",
            icon_name="microphone",
            icon_size="1.4rem",
            pause_threshold=1.2,
            sample_rate=44100,
        )

    with clear_col:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if st.button("Clear", type="secondary", use_container_width=True):
            AudioState.clear()
            st.experimental_rerun()

    if audio_bytes:
        if AudioState.needs_update(audio_bytes):
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(audio_bytes)
            AudioState.set_audio(audio_bytes, transcript)

    stored_audio = AudioState.get_audio()
    transcript_text = AudioState.get_transcript()

    if stored_audio:
        st.audio(stored_audio, format="audio/wav")
        if transcript_text:
            st.markdown("**Voice transcript**")
            st.markdown(
                f"<div class='entry-text'>{transcript_text}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("Transcription unavailable. Ensure the Whisper model is installed on the server.")


def _validate_inputs(uploaded_files: List, text_input: str, has_audio: bool) -> Optional[str]:
    if not uploaded_files and not has_audio and not text_input.strip():
        return "Add at least one photo, video, voice note, or typed note before saving."
    return None


def _handle_save(class_name: str, selected_date: dt.date, uploaded_files: List, text_input: str) -> None:
    audio_bytes = AudioState.get_audio()
    has_audio = audio_bytes is not None
    transcript_text = AudioState.get_transcript()
    validation_error = _validate_inputs(uploaded_files, text_input, has_audio)
    if validation_error:
        st.warning(validation_error)
        return

    entry_dir = ensure_entry_dir(class_name, selected_date)
    save_uploaded_files(entry_dir, uploaded_files)

    if has_audio and audio_bytes:
        save_audio(entry_dir, audio_bytes)
        if transcript_text:
            save_text(entry_dir, "voice_transcript.txt", transcript_text)

    if text_input.strip():
        save_text(entry_dir, "notes.txt", text_input)

    st.success("Entry saved to your class gallery.")

    AudioState.clear()
    st.session_state.pop("notes_input", None)
    st.experimental_rerun()



def main() -> None:
    st.set_page_config(
        page_title="Class Recorder",
        page_icon="🎒",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    inject_base_css()
    _render_header()

    with st.container():
        st.markdown("<div class='media-pill'>Class & Date</div>", unsafe_allow_html=True)
        st.markdown("<div class='slim-label'>", unsafe_allow_html=True)
        class_name = st.selectbox(
            "Choose class",
            CLASS_OPTIONS,
            key="class_select",
            label_visibility="collapsed",
        )
        today = dt.date.today()
        selected_date = st.date_input(
            "Choose date",
            value=st.session_state.get("date_picker", today),
            key="date_picker",
            help="Defaulting to today. Use the picker if you're logging a previous day.",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='media-pill' style='margin-top:1.4rem;'>Add media</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Add photos or video",
        accept_multiple_files=True,
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
            "heic",
            "mp4",
            "mov",
            "m4v",
            "avi",
            "mkv",
            "webm",
        ],
        key="media_uploader",
    )

    st.markdown("<div class='media-pill' style='margin-top:1.4rem;'>Typed notes</div>", unsafe_allow_html=True)
    st.markdown("<div class='compact-text-area'>", unsafe_allow_html=True)
    text_input = st.text_area(
        "Add quick context",
        key="notes_input",
        placeholder="Optional: jot down reminders, procedures, or observations.",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    _render_recorder_controls()

    class_info = CLASS_BY_NAME[class_name]
    st.markdown(
        f"<div style='margin-top:1.2rem;font-size:0.8rem;color:rgba(15,23,42,0.55);'>Files will be saved under <code>{class_info.slug}/{selected_date.isoformat()}</code>.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    save_button = st.button("Save entry", use_container_width=True)
    if save_button:
        _handle_save(class_name, selected_date, uploaded_files or [], text_input)


if __name__ == "__main__":
    main()
