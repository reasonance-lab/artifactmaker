"""Audio transcription helpers using Faster Whisper."""

from __future__ import annotations

import hashlib
import os
import tempfile
from typing import Optional

import streamlit as st

try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover - handled at runtime when dependency missing
    WhisperModel = None  # type: ignore


def _hash_audio(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@st.cache_resource(show_spinner=False)
def load_whisper_model() -> Optional[WhisperModel]:
    if WhisperModel is None:
        return None
    model_size = os.environ.get("WHISPER_MODEL_SIZE", "small")
    compute_type = os.environ.get("WHISPER_COMPUTE_TYPE", "int8_float16")
    device = os.environ.get("WHISPER_DEVICE", "cpu")
    return WhisperModel(model_size, device=device, compute_type=compute_type)


def transcribe_audio(audio_bytes: bytes) -> Optional[str]:
    """Transcribe raw audio bytes with the configured Whisper model."""

    model = load_whisper_model()
    if model is None:
        return None

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    try:
        segments, info = model.transcribe(temp_audio_path)
    finally:
        try:
            os.remove(temp_audio_path)
        except OSError:
            pass
    text_fragments = [segment.text.strip() for segment in segments if segment.text]
    transcript = " ".join(text_fragments).strip()
    return transcript or None


class AudioState:
    """Wrapper to keep track of the latest audio hash in session state."""

    state_key_bytes = "audio_bytes"
    state_key_hash = "audio_hash"
    state_key_transcript = "audio_transcript"

    @classmethod
    def set_audio(cls, audio_bytes: bytes, transcript: Optional[str]) -> None:
        st.session_state[cls.state_key_bytes] = audio_bytes
        st.session_state[cls.state_key_hash] = _hash_audio(audio_bytes)
        st.session_state[cls.state_key_transcript] = transcript

    @classmethod
    def needs_update(cls, audio_bytes: bytes) -> bool:
        current_hash = cls.get_hash()
        incoming_hash = _hash_audio(audio_bytes)
        return current_hash != incoming_hash

    @classmethod
    def clear(cls) -> None:
        for key in (cls.state_key_bytes, cls.state_key_hash, cls.state_key_transcript):
            st.session_state.pop(key, None)

    @classmethod
    def get_audio(cls) -> Optional[bytes]:
        return st.session_state.get(cls.state_key_bytes)

    @classmethod
    def get_transcript(cls) -> Optional[str]:
        return st.session_state.get(cls.state_key_transcript)

    @classmethod
    def get_hash(cls) -> Optional[str]:
        return st.session_state.get(cls.state_key_hash)

