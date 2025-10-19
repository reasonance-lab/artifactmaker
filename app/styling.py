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

header[data-testid="stHeader"] {
    background: transparent;
    box-shadow: none;
}

header[data-testid="stHeader"] div[data-testid="stToolbar"] {
    right: 0.8rem;
    top: 0.4rem;
}

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

.field-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(15, 23, 42, 0.55);
    margin-bottom: 0.35rem;
}

.class-date-row {
    margin-bottom: 0.6rem;
}

.class-date-row [data-testid="column"] {
    padding-top: 0 !important;
}

.class-date-row [data-testid="column"] > div {
    width: 100%;
    display: flex;
    flex-direction: column;
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

.gallery-date {
    position: relative;
    margin-top: 1.8rem;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.2rem;
}

.gallery-date::before,
.gallery-date::after {
    content: "";
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, rgba(14, 165, 233, 0), rgba(14, 165, 233, 0.45));
}

.gallery-date::after {
    background: linear-gradient(270deg, rgba(14, 165, 233, 0), rgba(14, 165, 233, 0.45));
}

.gallery-date span {
    font-size: 0.92rem;
    font-weight: 600;
    color: rgba(15, 23, 42, 0.76);
    padding: 0.45rem 1.35rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.22), rgba(14, 165, 233, 0.08));
    box-shadow: 0 8px 24px rgba(14, 165, 233, 0.12);
}

.gallery-slider {
    margin-top: 1.8rem;
}

.gallery-slider [data-testid="column"] {
    display: flex;
    align-items: stretch;
    justify-content: center;
}

.gallery-slide {
    width: 100%;
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(241, 245, 255, 0.95));
    border-radius: 22px;
    padding: 1.4rem 1.6rem 1rem;
    box-shadow: 0 22px 45px rgba(15, 23, 42, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.16);
}

.gallery-slide .entry-card {
    background: transparent;
    box-shadow: none;
    padding: 0;
    margin-bottom: 0;
}

.gallery-slide .entry-text {
    font-size: 0.95rem;
}

.slider-arrow {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.slider-arrow .stButton button {
    width: 3.1rem;
    height: 3.1rem;
    border-radius: 50%;
    border: none;
    font-size: 1.6rem;
    font-weight: 500;
    color: rgba(15, 23, 42, 0.82);
    background: radial-gradient(circle at 30% 30%, rgba(59, 130, 246, 0.18), rgba(59, 130, 246, 0.08));
    box-shadow: 0 12px 30px rgba(59, 130, 246, 0.22);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.slider-arrow .stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 35px rgba(59, 130, 246, 0.28);
}

.slider-arrow .stButton button:disabled {
    opacity: 0.35;
    cursor: not-allowed;
    box-shadow: none;
}

.slider-counter {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.82rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: rgba(71, 85, 105, 0.85);
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
}
</style>
"""


def inject_base_css() -> None:
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def format_entry_time(timestamp: datetime) -> str:
    return timestamp.strftime("%I:%M %p").lstrip("0")
