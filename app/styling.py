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
    --card-shadow: 0 8px 32px rgba(15, 23, 42, 0.08);
    --card-shadow-hover: 0 16px 48px rgba(15, 23, 42, 0.14);
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-accent: linear-gradient(135deg, rgba(14, 165, 233, 0.22), rgba(14, 165, 233, 0.08));
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

body {
    background: linear-gradient(180deg, #f5f5f5 0%, #f0f4ff 40%, #ffffff 100%);
}

/* Smooth transitions for all interactive elements */
* {
    transition: var(--transition-smooth);
}

section.main > div {
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 720px;
}

/* REMOVE ALL HORIZONTAL DIVIDERS/BARS */
.stHorizontalBlock {
    gap: 0 !important;
}

/* Hide all empty vertical blocks that create spacing/bars */
div[data-testid="stVerticalBlock"]:empty,
div[data-testid="stVerticalBlockBorderWrapper"]:empty {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove spacing between main container children */
section.main > div > div > div > div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* Remove any hr elements */
hr {
    display: none !important;
}

/* Target specific empty blocks between sections */
.form-section-card ~ div:empty,
.hero-section ~ div:empty {
    display: none !important;
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
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
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
    margin-bottom: 0.5rem;
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


/* Media badges */
.media-badges {
    display: flex;
    justify-content: center;
    gap: 0.4rem;
    margin-bottom: 0.6rem;
    flex-wrap: wrap;
}

.media-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: var(--gradient-accent);
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
    transition: transform 0.2s ease;
}

.media-badge:hover {
    transform: scale(1.15);
}


/* Improved empty state with animation */
.empty-state {
    margin-top: 3rem;
    padding: 2.5rem 2rem;
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(241, 245, 255, 0.9));
    border: 2px dashed rgba(14, 165, 233, 0.3);
    color: rgba(15, 23, 42, 0.72);
    font-size: 0.95rem;
    line-height: 1.6;
    text-align: center;
    box-shadow: 0 12px 32px rgba(14, 165, 233, 0.08);
    animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Enhanced slideshow with better animations */
.gallery-slider {
    margin-top: 1.2rem;
    margin-bottom: 1.5rem;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Gallery sections styling - match homepage containers */
.sections-container [data-testid="stVerticalBlock"]:has([data-testid="element-container"] .section-header) > [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: slideInUp 0.5s ease;
}

.sections-container [data-testid="stVerticalBlock"]:has([data-testid="element-container"] .section-header):hover > [data-testid="stVerticalBlockBorderWrapper"] {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
}

/* Improved slider arrows */
.slider-arrow .stButton button {
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    border: none;
    font-size: 1.8rem;
    font-weight: 500;
    color: rgba(15, 23, 42, 0.82);
    background: radial-gradient(circle at 30% 30%, rgba(102, 126, 234, 0.22), rgba(102, 126, 234, 0.12));
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.slider-arrow .stButton button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.32);
    background: radial-gradient(circle at 30% 30%, rgba(102, 126, 234, 0.3), rgba(102, 126, 234, 0.18));
}

.slider-arrow .stButton button:active {
    transform: translateY(-1px) scale(1.02);
}

.slider-arrow .stButton button:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

/* Enhanced slider counter */
.slider-counter {
    text-align: center;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-weight: 600;
    color: rgba(102, 126, 234, 0.85);
    background: var(--gradient-accent);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    display: inline-block;
    margin-left: 50%;
    transform: translateX(-50%);
}

/* Loading skeleton animation */
@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }
    100% {
        background-position: 1000px 0;
    }
}

.loading-skeleton {
    animation: shimmer 2s infinite;
    background: linear-gradient(to right, #f0f0f0 8%, #f8f8f8 18%, #f0f0f0 33%);
    background-size: 1000px 100%;
}


/* ===== HOME PAGE ENHANCEMENTS ===== */

/* Hero Section - Compact height, readable fonts */
.hero-section {
    text-align: center;
    padding: 0.8rem 1rem 0.7rem;
    margin: -1.2rem -2rem 0.8rem;
    background: var(--gradient-primary);
    border-radius: 0 0 20px 20px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    animation: heroFadeIn 0.4s ease;
}

@keyframes heroFadeIn {
    from {
        opacity: 0;
        transform: translateY(-5px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-icon {
    font-size: 2.5rem;
    margin-bottom: 0.3rem;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.app-title-hero {
    font-size: 1.6rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.2rem;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.app-subtitle-hero {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.95);
    font-weight: 400;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.3;
}

/* Sections Container - prevents Streamlit auto-separators */
.sections-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

/* Form Section Cards - Target st.container by key */
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-class-date-section) > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-media-upload-section) > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-typed-notes-section) > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-voice-recorder-section) > [data-testid="stVerticalBlockBorderWrapper"],
.form-section-card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 0;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: slideInUp 0.5s ease;
}

/* Hover effect for keyed containers */
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-class-date-section):hover > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-media-upload-section):hover > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-typed-notes-section):hover > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-voice-recorder-section):hover > [data-testid="stVerticalBlockBorderWrapper"] {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.form-section-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
}

/* Special styling for voice recorder section */
[data-testid="stVerticalBlock"]:has([data-testid="element-container"] .st-key-voice-recorder-section) > [data-testid="stVerticalBlockBorderWrapper"],
.recorder-section {
    border: 2px solid rgba(102, 126, 234, 0.2);
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(241, 245, 255, 0.95));
}

/* Section Headers */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: rgba(15, 23, 42, 0.85);
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 2px solid rgba(102, 126, 234, 0.15);
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.section-icon {
    font-size: 1.3rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: var(--gradient-accent);
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
}

/* File Count Badge */
.file-count-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    margin-top: 0.5rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.08));
    color: rgba(22, 101, 52, 0.95);
    font-size: 0.85rem;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.15);
    animation: popIn 0.3s ease;
}

@keyframes popIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Save Path Info */
.save-path-info {
    text-align: center;
    padding: 0.9rem 1.2rem;
    margin: 1.5rem 0 1rem;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(14, 165, 233, 0.05));
    border: 1px solid rgba(14, 165, 233, 0.2);
    font-size: 0.88rem;
    color: rgba(15, 23, 42, 0.75);
}

.save-path-info code {
    background: rgba(102, 126, 234, 0.1);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    color: rgba(102, 126, 234, 0.95);
    font-weight: 600;
}

.info-icon {
    font-size: 1.1rem;
    margin-right: 0.4rem;
}

/* Enhanced Save Button */
.save-button-container {
    margin: 1.5rem 0;
}

.save-button-container .stButton button {
    height: 3.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.save-button-container .stButton button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.45) !important;
}

.save-button-container .stButton button:active {
    transform: translateY(0) scale(0.98);
}

/* Enhanced Form Controls */
.stSelectbox > div[data-baseweb="select"] > div,
.stDateInput > div > div > input,
.stFileUploader section,
.stTextArea textarea {
    border: 2px solid rgba(102, 126, 234, 0.15) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stSelectbox > div[data-baseweb="select"] > div:hover,
.stDateInput > div > div > input:hover,
.stFileUploader section:hover,
.stTextArea textarea:hover {
    border-color: rgba(102, 126, 234, 0.3) !important;
}

.stSelectbox > div[data-baseweb="select"] > div:focus-within,
.stDateInput > div > div > input:focus,
.stFileUploader section:focus-within,
.stTextArea textarea:focus {
    border-color: rgba(102, 126, 234, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* File Uploader Styling */
.stFileUploader section {
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.5), rgba(248, 250, 252, 0.5));
    backdrop-filter: blur(5px);
}

.stFileUploader section button {
    background: var(--gradient-accent) !important;
    color: rgba(15, 23, 42, 0.85) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: var(--transition-smooth) !important;
}

.stFileUploader section button:hover {
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.3), rgba(14, 165, 233, 0.15)) !important;
    transform: scale(1.05);
}

/* Audio Recorder Enhancements */
.recorder-controls {
    margin-top: 0;
}

.recorder-controls .stButton button {
    border-radius: 12px !important;
    font-weight: 500 !important;
    transition: var(--transition-smooth) !important;
}

/* Enhanced Captions */
.stCaption {
    font-size: 0.85rem;
    color: rgba(15, 23, 42, 0.6);
    font-style: italic;
}

/* Improved Inline Feedback with Animation */
.inline-feedback {
    margin-top: 1rem;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    font-size: 0.9rem;
    line-height: 1.5;
    animation: slideInDown 0.4s ease;
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.inline-feedback.success {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.08));
    border: 2px solid rgba(34, 197, 94, 0.3);
    color: rgba(22, 101, 52, 0.95);
    box-shadow: 0 4px 16px rgba(34, 197, 94, 0.15);
}

.inline-feedback.warning {
    background: linear-gradient(135deg, rgba(250, 204, 21, 0.15), rgba(250, 204, 21, 0.08));
    border: 2px solid rgba(250, 204, 21, 0.35);
    color: rgba(113, 63, 18, 0.95);
    box-shadow: 0 4px 16px rgba(250, 204, 21, 0.15);
}

.inline-feedback.error {
    background: linear-gradient(135deg, rgba(248, 113, 113, 0.15), rgba(248, 113, 113, 0.08));
    border: 2px solid rgba(248, 113, 113, 0.4);
    color: rgba(127, 29, 29, 0.95);
    box-shadow: 0 4px 16px rgba(248, 113, 113, 0.15);
}

.inline-feedback.info {
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(14, 165, 233, 0.08));
    border: 2px solid rgba(14, 165, 233, 0.3);
    color: rgba(21, 94, 117, 0.95);
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.15);
}

@media (max-width: 640px) {
    section.main > div {
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }
    .entry-media-grid {
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }

    .slider-arrow .stButton button {
        width: 2.8rem;
        height: 2.8rem;
        font-size: 1.4rem;
    }

    /* Mobile Home Page Adjustments */
    .hero-section {
        padding: 0.7rem 0.8rem 0.6rem;
        margin: -1.2rem -1rem 0.7rem;
        border-radius: 0 0 16px 16px;
    }

    .hero-icon {
        font-size: 2rem;
        margin-bottom: 0.25rem;
    }

    .app-title-hero {
        font-size: 1.4rem;
        margin-bottom: 0.2rem;
    }

    .app-subtitle-hero {
        font-size: 0.85rem;
    }

    .sections-container {
        gap: 1rem;
    }

    .form-section-card {
        padding: 1.2rem;
        margin-bottom: 0;
    }

    .section-header {
        font-size: 1rem;
    }

    .section-icon {
        width: 2rem;
        height: 2rem;
        font-size: 1.1rem;
    }

    .save-button-container .stButton button {
        height: 3rem;
        font-size: 1rem;
    }
}
</style>
"""


def inject_base_css() -> None:
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def format_entry_time(timestamp: datetime) -> str:
    return timestamp.strftime("%I:%M %p").lstrip("0")
