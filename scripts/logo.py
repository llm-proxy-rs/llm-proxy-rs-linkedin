#!/usr/bin/env python3
"""Wide copper-pipe banner for the llm-proxy-rs README."""

from __future__ import annotations

import sys
from pathlib import Path

import cairo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipe_font import draw_line, measure, wash

ROOT = Path("/home/packer/llm-proxy-rs")
OUT = ROOT / "docs" / "logo.png"
W, H = 1280, 280
SIZE, TRACK = 88, 0.08


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    wash(cr, W, H)
    text = "LLM-PROXY-RS"
    tw = measure(text, SIZE, TRACK)
    draw_line(cr, text, (W - tw) / 2, (H - SIZE) / 2, SIZE, TRACK)
    surf.write_to_png(str(OUT))
    print(OUT)


if __name__ == "__main__":
    main()
