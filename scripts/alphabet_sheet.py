#!/usr/bin/env python3
"""Preview every pipe glyph."""

from __future__ import annotations

import sys
from pathlib import Path

import cairo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipe_font import GLYPHS, draw_letter, wash

ROOT = Path(__file__).resolve().parents[1]
W = H = 1080


def main() -> None:
    chars = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ-." if c in GLYPHS]
    cols = 6
    rows = (len(chars) + cols - 1) // cols
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    wash(cr)
    cell_w, cell_h = W / cols, (H - 40) / rows
    size = min(cell_w, cell_h) * 0.62
    for i, ch in enumerate(chars):
        col, row = i % cols, i // cols
        x = col * cell_w + (cell_w - size * GLYPHS[ch].width) / 2
        y = 20 + row * cell_h + (cell_h - size) / 2
        draw_letter(cr, ch, x, y, size)
    path = ROOT / "docs" / "pipe-alphabet.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    surf.write_to_png(str(path))
    print(path)


if __name__ == "__main__":
    main()
