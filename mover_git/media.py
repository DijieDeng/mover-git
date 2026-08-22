from datetime import datetime
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS

MEDIA_FILE_TYPES = (".jpg", ".jpeg", ".png", ".heic", ".mp4", ".mov", ".avi", ".aae")


def is_supported_media(path: Path) -> bool:
    """
    determine whether a path uses a supported media extension
    :param path: file path to inspect
    :returns: whether the path is a supported media type
    """
    return path.suffix.lower() in MEDIA_FILE_TYPES


def sanitize_timestamp_filename(value: datetime) -> str:
    """
    format a datetime as a filename safe timestamp
    :param value: datetime to format
    :returns: timestamp suitable for a filename
    """
    return value.strftime("%Y-%m-%d %H_%M_%S")


def get_media_datetime(file_path: Path) -> datetime:
    """
    retrieve an image capture time or filesystem modification time
    :param file_path: media file to inspect
    :returns: best available datetime for the file
    """
    if file_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic"}:
        try:
            with Image.open(file_path) as image:
                exif = image.getexif()
                for field in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
                    for tag, value in exif.items():
                        if TAGS.get(tag) == field:
                            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except (OSError, TypeError, ValueError):
            pass
    return datetime.fromtimestamp(file_path.stat().st_mtime)


def build_target_path(
    destination: Path,
    entry_path: Path,
    relative_path: Path,
    used_paths: set[Path],
    organize: bool,
    supported_only: bool,
    use_date_folder: bool,
    rename_to_timestamp: bool,
    media_datetime: datetime | None = None,
) -> Path:
    """
    build a collision safe destination path
    :param destination: destination root directory
    :param entry_path: source file path
    :param relative_path: source relative path
    :param used_paths: destination paths assigned during this operation
    :param organize: whether media organization is enabled
    :param supported_only: whether organization applies only to supported media
    :param use_date_folder: whether to create a date folder
    :param rename_to_timestamp: whether to rename the file with its timestamp
    :param media_datetime: optional precomputed media datetime
    :returns: available destination path
    """
    original = destination / relative_path
    if not organize or (supported_only and not is_supported_media(entry_path)):
        candidate = original
    else:
        value = media_datetime or get_media_datetime(entry_path)
        folder = destination / value.strftime("%Y-%m-%d") if use_date_folder else original.parent
        name = sanitize_timestamp_filename(value) if rename_to_timestamp else entry_path.stem
        candidate = folder / f"{name}{entry_path.suffix}"
    target = candidate
    counter = 1
    while target.exists() or target in used_paths:
        target = candidate.with_name(f"{candidate.stem}_{counter}{candidate.suffix}")
        counter += 1
    used_paths.add(target)
    return target
