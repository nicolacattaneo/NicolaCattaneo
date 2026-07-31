import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from rembg import remove
except ImportError:
    remove = None


OUT = Path("source-prepped.png")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/prep_photo.py source-photo.jpg")

    source = Path(sys.argv[1])
    image = Image.open(source).convert("RGBA")
    image = ImageOps.exif_transpose(image)
    image.thumbnail((900, 1100), Image.Resampling.LANCZOS)

    if remove is not None:
        cutout = remove(image)
    else:
        cutout = image

    white = Image.new("RGBA", cutout.size, (255, 255, 255, 255))
    flattened = Image.alpha_composite(white, cutout).convert("L")
    arr = np.array(flattened)

    if cv2 is not None:
        clahe = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8, 8))
        enhanced = clahe.apply(arr)
        result = Image.fromarray(enhanced)
    else:
        result = ImageOps.autocontrast(flattened, cutoff=2)
        result = ImageOps.equalize(result)
        result = ImageEnhance.Contrast(result).enhance(1.45)
        result = result.filter(ImageFilter.UnsharpMask(radius=1.4, percent=120, threshold=3))

    result.save(OUT)


if __name__ == "__main__":
    main()
