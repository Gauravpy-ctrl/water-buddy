# image_customizer.py
from __future__ import annotations

from pathlib import Path

from PIL import Image


def prepare_custom_image(source_path: Path, dest_path: Path, size: int = 220) -> None:
    """Fit an arbitrary user-supplied image onto a transparent square
    canvas and save it as a PNG.

    Alpha is binarized (hard 0/255, no partial-transparency edges) so it
    matches the bundled sprites -- a soft/antialiased edge would pick up
    the window's colorkey transparency color as a visible fringe when Tk
    composites it (see the NEAREST-resize fix in animations.py for the
    same issue on the original assets).
    """
    image = Image.open(source_path).convert("RGBA")
    image.thumbnail((size, size), Image.NEAREST)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - image.width) // 2, (size - image.height) // 2)
    canvas.paste(image, offset, image)

    alpha = canvas.split()[3]
    alpha = alpha.point(lambda a: 255 if a >= 128 else 0)
    canvas.putalpha(alpha)

    canvas.save(dest_path)
