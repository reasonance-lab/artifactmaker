"""Streamlit entry point for the classroom media recorder."""

from __future__ import annotations

import base64
import datetime as dt
from typing import Dict, List, Optional, Tuple

import streamlit as st
from audio_recorder_streamlit import audio_recorder

from app.constants import CLASS_BY_NAME, CLASS_OPTIONS
from app.storage import (
    ensure_entry_dir,
    save_audio,
    save_captured_media,
    save_text,
    save_uploaded_files,
)
from app.styling import inject_base_css
from app.transcription import AudioState, TranscriptionRuntimeError, transcribe_audio


def _display_feedback(feedback: Optional[Tuple[str, str]]) -> None:
    if not feedback:
        return
    status, message = feedback
    if status == "success":
        st.success(message)
    elif status == "warning":
        st.warning(message)
    elif status == "error":
        st.error(message)
    else:
        st.info(message)


def _emit_toast(feedback: Optional[Tuple[str, str]]) -> None:
    if not feedback:
        return
    icon_map = {"success": "✅", "warning": "⚠️", "error": "❌", "info": "ℹ️"}
    if hasattr(st, "toast"):
        icon = icon_map.get(feedback[0], "ℹ️")
        st.toast(feedback[1], icon=icon)
    else:
        _display_feedback(feedback)


def _render_inline_feedback(feedback: Optional[Tuple[str, str]]) -> None:
    if not feedback:
        return
    status, message = feedback
    st.markdown(
        f"<div class='inline-feedback {status}'>{message}</div>",
        unsafe_allow_html=True,
    )


def _render_captured_previews(captures: List[Dict[str, object]]) -> None:
    if not captures:
        return

    html_parts = ["<div class='captured-grid'>"]
    for capture in captures:
        raw_bytes = capture.get("bytes")
        if not isinstance(raw_bytes, (bytes, bytearray)):
            continue
        mime = str(capture.get("mime") or "image/jpeg")
        encoded = base64.b64encode(bytes(raw_bytes)).decode("ascii")
        html_parts.append(
            f"<img src='data:{mime};base64,{encoded}' alt='Captured photo' />"
        )
    html_parts.append("</div>")
    if len(html_parts) > 2:
        st.markdown("".join(html_parts), unsafe_allow_html=True)


def _render_header() -> None:
    st.markdown("<div class='app-title'>Classroom Capture</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='app-subtitle'>Quickly capture labs, experiments, and reflections in one place.</div>",
        unsafe_allow_html=True,
    )


def _render_recorder_controls() -> None:
    st.markdown("<div class='media-pill'>🎙️ Voice recorder</div>", unsafe_allow_html=True)

    st.session_state.setdefault("transcription_request", False)
    st.session_state.setdefault("transcription_error", None)
    st.session_state.setdefault("transcription_error_detail", None)

    st.markdown("<div class='recorder-controls'>", unsafe_allow_html=True)
    record_col, clear_col = st.columns([4, 1], gap="small")

    with record_col:
        audio_bytes = audio_recorder(
            text="Tap to record",
            recording_color="#ef4444",
            neutral_color="#0ea5e9",
            icon_name="microphone",
            icon_size="1.4rem",
            pause_threshold=6.0,
            sample_rate=44100,
        )

    with clear_col:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if st.button("Clear", key="clear_audio", type="secondary", use_container_width=True):
            AudioState.clear()
            st.session_state["transcription_request"] = False
            st.session_state.pop("transcription_error", None)
            st.session_state.pop("transcription_error_detail", None)
            st.session_state.pop("save_feedback_inline", None)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if audio_bytes and AudioState.needs_update(audio_bytes):
        AudioState.set_audio(audio_bytes, None)
        st.session_state["transcription_request"] = True
        st.session_state["transcription_error"] = None
        st.session_state["transcription_error_detail"] = None
        st.rerun()

    stored_audio = AudioState.get_audio()

    if stored_audio and st.session_state.get("transcription_request"):
        try:
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(stored_audio)
        except TranscriptionRuntimeError as exc:  # pragma: no cover - runtime safety net
            detail = str(exc.__cause__) if exc.__cause__ else str(exc)
            st.session_state["transcription_error"] = str(exc)
            st.session_state["transcription_error_detail"] = (
                detail if detail and detail != str(exc) else None
            )
            st.session_state["transcription_feedback"] = (
                "error",
                "Transcription failed. Review the warning below for details.",
            )
        except Exception as exc:  # pragma: no cover - runtime safety net
            st.session_state["transcription_error"] = (
                "Unexpected error while transcribing this clip."
            )
            st.session_state["transcription_error_detail"] = str(exc)
            st.session_state["transcription_feedback"] = (
                "error",
                "Transcription failed. Review the warning below for details.",
            )
        else:
            if transcript:
                AudioState.set_audio(stored_audio, transcript)
                st.session_state["transcription_error"] = None
                st.session_state["transcription_error_detail"] = None
                st.session_state["transcription_feedback"] = (
                    "success",
                    "Voice transcription ready.",
                )
            else:
                st.session_state["transcription_error"] = (
                    "Whisper returned an empty transcript. The audio will be stored without text."
                )
                st.session_state["transcription_error_detail"] = None
                st.session_state["transcription_feedback"] = (
                    "warning",
                    "Audio saved without a transcript. Check your Whisper configuration.",
                )
        finally:
            st.session_state["transcription_request"] = False

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
            error_message = st.session_state.get("transcription_error")
            detail_message = st.session_state.get("transcription_error_detail")
            if error_message:
                _render_inline_feedback(("error", error_message))
                if detail_message:
                    st.code(detail_message, language="text")
            if not st.session_state.get("transcription_request"):
                if st.button("Transcribe recording", key="retry_transcription", type="primary"):
                    st.session_state["transcription_request"] = True
                    st.session_state.pop("transcription_error", None)
                    st.session_state.pop("transcription_error_detail", None)
                    st.rerun()


def _validate_inputs(
    uploaded_files: List,
    text_input: str,
    has_audio: bool,
    camera_count: int,
) -> Optional[str]:
    if (
        not uploaded_files
        and camera_count == 0
        and not has_audio
        and not text_input.strip()
    ):
        return "Add at least one photo, video, voice note, or typed note before saving."
    return None


def _handle_save(
    class_name: str,
    selected_date: dt.date,
    uploaded_files: List,
    text_input: str,
    captured_media: List[Dict[str, object]],
) -> None:
    uploads = list(uploaded_files)
    camera_media = list(captured_media)
    audio_bytes = AudioState.get_audio()
    has_audio = audio_bytes is not None
    transcript_text = AudioState.get_transcript()
    validation_error = _validate_inputs(uploads, text_input, has_audio, len(camera_media))
    if validation_error:
        st.warning(validation_error)
        return

    class_info = CLASS_BY_NAME[class_name]
    entry_dir = ensure_entry_dir(class_name, selected_date)
    save_uploaded_files(entry_dir, uploads)
    if camera_media:
        save_captured_media(entry_dir, camera_media)

    if has_audio and audio_bytes:
        save_audio(entry_dir, audio_bytes)
        if transcript_text:
            save_text(entry_dir, "voice_transcript.txt", transcript_text)

    if text_input.strip():
        save_text(entry_dir, "notes.txt", text_input)

    summary_parts: List[str] = []
    if uploads:
        summary_parts.append(
            f"{len(uploads)} upload{'s' if len(uploads) != 1 else ''}"
        )
    if camera_media:
        summary_parts.append(
            f"{len(camera_media)} camera photo{'s' if len(camera_media) != 1 else ''}"
        )
    if has_audio:
        summary_parts.append("audio clip")
    if text_input.strip():
        summary_parts.append("typed notes")

    attachment_summary = f" ({', '.join(summary_parts)})" if summary_parts else ""
    feedback = (
        "success",
        f"Saved entry to {class_info.slug}/{selected_date.isoformat()}{attachment_summary}.",
    )
    st.session_state["save_feedback"] = feedback
    st.session_state["save_feedback_inline"] = feedback
    AudioState.clear()
    st.session_state.pop("notes_input", None)
    st.session_state["transcription_request"] = False
    st.session_state.pop("transcription_error", None)
    st.session_state.pop("transcription_error_detail", None)
    st.session_state["camera_media"] = []
    st.session_state["camera_capture"] = None
    st.session_state.pop("camera_status", None)
    st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Class Recorder",
        page_icon="🎒",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    inject_base_css()
    if "camera_media" not in st.session_state:
        st.session_state["camera_media"] = []

    if "save_feedback" in st.session_state:
        st.session_state["save_feedback_inline"] = st.session_state["save_feedback"]

    _display_feedback(st.session_state.pop("save_feedback", None))
    _emit_toast(st.session_state.pop("transcription_feedback", None))
    _render_header()

    st.markdown("<div class='media-pill'>Class & Date</div>", unsafe_allow_html=True)
    st.markdown("<div class='class-date-row'>", unsafe_allow_html=True)
    class_col, date_col = st.columns(2, gap="small")

    with class_col:
        st.caption("Class")
        class_name = st.selectbox(
            "Choose class",
            CLASS_OPTIONS,
            key="class_select",
            label_visibility="collapsed",
        )
    with date_col:
        st.caption("Date")
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
    st.caption(
        "Having trouble attaching a fresh photo or video from your phone camera? Use the quick capture below."
    )

    camera_capture = st.camera_input(
        "Capture a photo",
        key="camera_capture",
        help="Take a quick still photo from your device camera.",
    )
    if camera_capture:
        capture_bytes = camera_capture.getvalue()
        if capture_bytes:
            st.session_state["camera_media"].append(
                {
                    "name": camera_capture.name
                    or f"camera-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    "bytes": capture_bytes,
                    "mime": camera_capture.type or "image/jpeg",
                }
            )
            st.session_state["camera_status"] = (
                "success",
                "Added a camera photo to this entry.",
            )
            st.rerun()

    camera_status = st.session_state.pop("camera_status", None)
    _render_inline_feedback(camera_status)

    captured_media: List[Dict[str, object]] = st.session_state.get("camera_media", [])
    if captured_media:
        st.markdown("<div class='media-pill' style='margin-top:0.9rem;'>📸 Camera captures</div>", unsafe_allow_html=True)
        _render_captured_previews(captured_media)
        st.markdown("<div class='captured-actions'>", unsafe_allow_html=True)
        if st.button("Clear camera captures", key="clear_camera_captures", type="secondary"):
            st.session_state["camera_media"] = []
            st.session_state["camera_capture"] = None
            st.session_state["camera_status"] = (
                "info",
                "Camera captures cleared.",
            )
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
        _handle_save(
            class_name,
            selected_date,
            list(uploaded_files or []),
            text_input,
            captured_media,
        )

    _render_inline_feedback(st.session_state.get("save_feedback_inline"))


if __name__ == "__main__":
    main()
