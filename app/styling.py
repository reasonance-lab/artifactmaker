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
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(14, 165, 233, 0.08));
    color: rgba(15, 23, 42, 0.75);
    font-size: 0.8rem;
}

.class-date-row {
    margin-bottom: 0.6rem;
}

.class-date-row [data-testid="column"] > div {
    width: 100%;
}

.class-date-row .stSelectbox div[data-baseweb="select"] {
    border-radius: var(--primary-radius) !important;
    min-height: 2.75rem;
}

.class-date-row .stDateInput input {
    border-radius: var(--primary-radius) !important;
    min-height: 2.75rem;
}

.recorder-controls {
    margin-top: 1.2rem;
}

.recorder-controls [data-testid="column"]:last-of-type .stButton button {
    background: linear-gradient(135deg, #f87171, #dc2626);
    color: #fff;
    border: none;
}

.recorder-controls [data-testid="column"]:last-of-type .stButton button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
}

.inline-feedback {
    margin-top: 0.8rem;
    padding: 0.6rem 0.8rem;
    border-radius: var(--primary-radius);
    font-size: 0.85rem;
    line-height: 1.4;
}

.inline-feedback.success {
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.28);
    color: rgba(22, 101, 52, 0.95);
}

.inline-feedback.warning {
    background: rgba(250, 204, 21, 0.12);
    border: 1px solid rgba(250, 204, 21, 0.3);
    color: rgba(113, 63, 18, 0.95);
}

.inline-feedback.error {
    background: rgba(248, 113, 113, 0.12);
    border: 1px solid rgba(248, 113, 113, 0.35);
    color: rgba(127, 29, 29, 0.95);
}

.inline-feedback.info {
    background: rgba(14, 165, 233, 0.12);
    border: 1px solid rgba(14, 165, 233, 0.28);
    color: rgba(21, 94, 117, 0.95);
}

.captured-grid {
    margin-top: 0.8rem;
    display: grid;
    gap: 0.65rem;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
}

.captured-grid img {
    border-radius: var(--primary-radius);
    width: 100%;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
}

.captured-actions {
    margin-top: 0.4rem;
    text-align: right;
}

.captured-actions button[data-testid="baseButton-secondary"] {
    border-radius: 999px;
}

.gallery-date {
    margin-top: 1.8rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.gallery-date span {
    font-size: 0.9rem;
    font-weight: 600;
    color: rgba(15, 23, 42, 0.72);
    padding: 0.5rem 1.2rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(14, 165, 233, 0.05));
    box-shadow: inset 0 0 0 1px rgba(14, 165, 233, 0.2), 0 10px 30px rgba(14, 165, 233, 0.1);
}

.empty-state {
    margin-top: 1.6rem;
    padding: 1.1rem 1.25rem;
    border-radius: var(--primary-radius);
    background: rgba(14, 165, 233, 0.12);
    border: 1px dashed rgba(14, 165, 233, 0.4);
    color: rgba(15, 23, 42, 0.72);
    font-size: 0.9rem;
    line-height: 1.45;
}

.danger-zone {
    margin-top: 2rem;
    padding: 1.1rem 1.2rem;
    border-radius: var(--primary-radius);
    background: rgba(220, 38, 38, 0.08);
    border: 1px solid rgba(220, 38, 38, 0.25);
}

.danger-zone h3 {
    margin: 0 0 0.4rem;
    font-size: 0.95rem;
    color: rgba(153, 27, 27, 0.92);
}

.danger-zone p {
    font-size: 0.85rem;
    color: rgba(153, 27, 27, 0.85);
    margin-bottom: 0.75rem;
}

.danger-zone .stButton button {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    border: none;
    color: #fff;
}

.danger-zone .stButton button:hover {
    background: linear-gradient(135deg, #b91c1c, #991b1b);
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

.entry-warning {
    margin-top: 0.6rem;
    padding: 0.65rem 0.85rem;
    border-radius: var(--primary-radius);
    background: rgba(251, 191, 36, 0.15);
    border: 1px solid rgba(217, 119, 6, 0.2);
    color: rgba(113, 63, 18, 0.95);
    font-size: 0.85rem;
    line-height: 1.4;
}

@media (max-width: 640px) {
    section.main > div {
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }
    .entry-media-grid {
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
    .captured-grid {
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
}
</style>
"""


def inject_base_css() -> None:
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def format_entry_time(timestamp: datetime) -> str:
    return timestamp.strftime("%I:%M %p").lstrip("0")
