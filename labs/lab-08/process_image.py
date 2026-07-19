import sys
import os
from PIL import Image
import io
import base64

def process_image(path):
    with Image.open(path) as img:
        # write the size before processing to stderr
        size_before = os.path.getsize(path)
        print(f"Before: {img.size[0]}x{img.size[1]} px, {size_before / 1024:.1f} KB", file=sys.stderr)

        img = img.convert("RGB")  # Remove alpha channel
        img.thumbnail((1024, 1024))  # Proportional resize

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)

        # write the size after processing to stderr
        size_after = buffer.tell()
        print(f"After:  {img.size[0]}x{img.size[1]} px, {size_after / 1024:.1f} KB", file=sys.stderr)

        return base64.b64encode(buffer.getvalue()).decode("utf-8")