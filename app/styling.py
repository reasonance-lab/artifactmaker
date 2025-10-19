"""Reusable CSS and small UI helpers."""

from __future__ import annotations

from datetime import datetime

import streamlit as st


BASE_CSS = """
<style>
:root {
    --primary-radius: 14px;
    --card-bg: rgba(255,255,255,0.84);
    --accent-muted: rgba(0,0,0,0.35);
}

body {
    background: linear-gradient(180deg, #f5f5f5 0%, #f0f4ff 40%, #ffffff 100%);
}

section.main > div {
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 720px;
}

.stApp header {display: none;}

.app-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.1rem;
}

.app-subtitle {
    font-size: 0.85rem;
    color: var(--accent-muted);
    margin-bottom: 1.2rem;
}

.slim-label label {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

.compact-text-area textarea {
    min-height: 120px !important;
    border-radius: var(--primary-radius) !important;
}

.media-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background-color: rgba(15, 23, 42, 0.08);
    font-size: 0.8rem;
}

.gallery-date {
    margin-top: 1.8rem;
    margin-bottom: 0.6rem;
    padding-bottom: 0.2rem;
    border-bottom: 1px solid rgba(15, 23, 42, 0.08);
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
}

.gallery-date span {
    font-size: 0.95rem;
    font-weight: 600;
}

.entry-card {
    background: var(--card-bg);
    border-radius: var(--primary-radius);
    padding: 0.85rem 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
}

.entry-meta {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent-muted);
}

.entry-text {
    font-size: 0.9rem;
    margin-top: 0.6rem;
    margin-bottom: 0.6rem;
    line-height: 1.45;
}

.entry-media-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 0.6rem;
}

.entry-media-grid img, .entry-media-grid video {
    width: 100%;
    border-radius: 12px;
}

@media (max-width: 640px) {
    section.main > div {
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }
    .entry-media-grid {
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
}
</style>
"""


def inject_base_css() -> None:
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def format_entry_time(timestamp: datetime) -> str:
    return timestamp.strftime("%I:%M %p").lstrip("0")
