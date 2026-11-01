#!/usr/bin/env python3
"""Put your photo inside idcard.svg (SVG files shown via <img> cannot load
external images, so the photo must be embedded as base64).

Usage:  python scripts/embed_photo.py my_photo.jpg
Tip: use a small square photo (~300x300, under 150 KB) so the SVG stays light.
"""
import base64, re, sys, mimetypes, os
photo = sys.argv[1]
mime = mimetypes.guess_type(photo)[0] or "image/jpeg"
b64 = base64.b64encode(open(photo, "rb").read()).decode()
svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "idcard.svg")
svg = open(svg_path, encoding="utf-8").read()
img = (f'<image href="data:{mime};base64,{b64}" x="150" y="212" width="100" height="100" '
       f'preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip)"/>')
svg = re.sub(r"<!--PHOTO-->.*?<!--/PHOTO-->", img, svg, flags=re.S)
open(svg_path, "w", encoding="utf-8").write(svg)
print("Photo embedded in idcard.svg")
