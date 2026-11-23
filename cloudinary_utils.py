
import os
from pathlib import Path
from urllib.parse import urlparse

import cloudinary
import cloudinary.uploader


def configure_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )


def save_upload(file_obj, folder="ss-solar"):
    if not file_obj or not file_obj.filename:
        return None

    allowed = {"png", "jpg", "jpeg", "webp", "gif"}
    ext = Path(file_obj.filename).suffix.lower().lstrip(".")

    if ext not in allowed:
        return None

    configure_cloudinary()

    result = cloudinary.uploader.upload(
        file_obj,
        folder=folder,
        resource_type="image",
    )

    return result.get("secure_url")


def delete_cloudinary_image(image_url):
    if not image_url or "res.cloudinary.com" not in image_url:
        return False

    try:
        parsed = urlparse(image_url)
        parts = parsed.path.split("/upload/", 1)

        if len(parts) != 2:
            return False

        path = parts[1].split("/")
        
        # Skip Cloudinary version segment such as v123456789
        if path and path[0].startswith("v") and path[0][1:].isdigit():
            path = path[1:]

        public_id_with_ext = "/".join(path)
        public_id = str(Path(public_id_with_ext).with_suffix(""))

        configure_cloudinary()

        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="image",
        )

        return result.get("result") == "ok"

    except Exception:
        return False
