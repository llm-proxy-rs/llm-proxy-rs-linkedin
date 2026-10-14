#!/usr/bin/env python3
"""LinkedIn 1080×1080 plates: copper pipe letters for llm-proxy-rs."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import cairo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipe_font import COPPER, TAUPE, draw_centered, draw_line, footer, measure, serif, wash

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
W = H = 1080


def surface() -> tuple[cairo.ImageSurface, cairo.Context]:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    wash(cr)
    return surf, cr


def centered_stack(cr: cairo.Context, lines: tuple[str, ...], y: float, size: float, tracking: float, gap: float) -> float:
    for line in lines:
        tw = measure(line, size, tracking)
        draw_line(cr, line, (W - tw) / 2, y, size, tracking)
        y += size + gap
    return y


def round_rect(cr: cairo.Context, x: float, y: float, w: float, h: float, r: float) -> None:
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def bash_block(cr: cairo.Context, y: float, lines: tuple[str, ...]) -> None:
    face = "Liberation Mono"
    size = 26
    cr.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    longest = 0.0
    for line in lines:
        xb, _yb, tw, _th, _xa, _ya = cr.text_extents("$ " + line)
        longest = max(longest, tw - xb)
    pad_x, pad_top, pad_bot, row = 28.0, 72.0, 28.0, 44.0
    w = longest + pad_x * 2
    h = pad_top + row * (len(lines) - 1) + pad_bot + 22
    x = (W - w) / 2

    round_rect(cr, x, y, w, h, 12)
    cr.set_source_rgb(0.96, 0.92, 0.86)
    cr.fill_preserve()
    cr.set_source_rgb(*TAUPE)
    cr.set_line_width(1.5)
    cr.stroke()
    serif(cr, "bash", x + pad_x, y + 36, 22, italic=True, mono=True)
    ty = y + 94
    for line in lines:
        cr.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(size)
        cr.set_source_rgb(*COPPER)
        cr.move_to(x + pad_x, ty)
        cr.show_text("$ ")
        cr.set_source_rgb(*TAUPE)
        cr.show_text(line)
        ty += row


def verse_card(path: Path) -> None:
    surf, cr = surface()
    draw_centered(cr, "LLM-", 118, 140, tracking=0.10)
    draw_centered(cr, "PROXY", 278, 124, tracking=0.08)
    draw_centered(cr, "-RS", 424, 124, tracking=0.14)
    centered_stack(cr, ("A LLM PROXY", "WRITTEN IN RUST"), 600, 40, 0.10, 18)
    serif(cr, "Visit the GitHub repository", 0, 770, 28, italic=True, center=True)
    serif(cr, "github.com/llm-proxy-rs/llm-proxy-rs", 0, 812, 28, center=True)
    footer(cr)
    surf.write_to_png(str(path))


def model_row(cr: cairo.Context, name: str, y: float, latest: bool = True) -> None:
    name_s, tag_s, gap = 32.0, 16.0, 14.0
    cr.select_font_face("Liberation Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(name_s)
    nxb, nyb, nw, nth, _nxa, _nya = cr.text_extents(name)
    x = (W - (nw - nxb)) / 2 - nxb
    serif(cr, name, x, y, name_s)
    if not latest:
        return
    draw_line(
        cr,
        "LATEST",
        x + nxb + (nw - nxb) + gap,
        y + nyb + nth / 2 - tag_s / 2,
        tag_s,
        tracking=0.10,
    )


def dated_card(path: Path) -> None:
    """Same note, plus Claude Sonnet 5.5 and Claude Haiku 5.5 tagged LATEST."""
    surf, cr = surface()
    label = "LLM-PROXY-RS"
    ls = 72
    tw = measure(label, ls, tracking=0.08)
    draw_line(cr, label, (W - tw) / 2, 56, ls, tracking=0.08)

    hs = 32
    below = 92
    models_y = 196
    install_y = 560
    draw_centered(cr, "SUPPORTED MODELS", models_y, hs, tracking=0.10)
    my = models_y + below
    for name, latest in (
        ("Claude Fable 5.1", False),
        ("Claude Opus 5.5", False),
        ("Claude Sonnet 5.5", True),
        ("Claude Haiku 5.5", True),
        ("GPT-6 Astra", False),
        ("GPT-6 Sol", False),
        ("GPT-6 Luna", False),
    ):
        model_row(cr, name, my, latest)
        my += 36

    draw_centered(cr, "INSTALL", install_y, hs, tracking=0.12)
    bash_block(
        cr,
        install_y + below - 8,
        (
            "git clone https://github.com/llm-proxy-rs/llm-proxy-rs",
            "cd llm-proxy-rs",
            "cargo run -p server",
        ),
    )
    footer(cr)
    surf.write_to_png(str(path))


def note_card(path: Path) -> None:
    surf, cr = surface()
    label = "LLM-PROXY-RS"
    ls = 72
    tw = measure(label, ls, tracking=0.08)
    draw_line(cr, label, (W - tw) / 2, 56, ls, tracking=0.08)

    hs = 32
    below = 92
    models_y = 196
    install_y = 498
    draw_centered(cr, "SUPPORTED MODELS", models_y, hs, tracking=0.10)
    my = models_y + below
    for name, latest in (
        ("Claude Fable 5.1", False),
        ("Claude Opus 5.5", True),
        ("GPT-6 Astra", False),
        ("GPT-6 Sol", True),
        ("GPT-6 Luna", True),
    ):
        model_row(cr, name, my, latest)
        my += 40

    draw_centered(cr, "INSTALL", install_y, hs, tracking=0.12)
    bash_block(
        cr,
        install_y + below,
        (
            "git clone https://github.com/llm-proxy-rs/llm-proxy-rs",
            "cd llm-proxy-rs",
            "cargo run -p server",
        ),
    )
    footer(cr)
    surf.write_to_png(str(path))


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    a = DOCS / "linkedin-llm-proxy-rs.png"
    b = DOCS / "linkedin-llm-proxy-rs-note.png"
    c = DOCS / "linkedin-llm-proxy-rs-note-2026-10-13.png"
    verse_card(a)
    note_card(b)
    dated_card(c)
    print(a)
    print(b)
    print(c)


if __name__ == "__main__":
    main()
