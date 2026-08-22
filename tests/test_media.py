from datetime import datetime
from pathlib import Path

from mover_git.media import build_target_path, is_supported_media, sanitize_timestamp_filename


def test_supported_media_is_case_insensitive() -> None:
    """
    verify media extension matching ignores case
        :returns: nothing
    """
    assert is_supported_media(Path("photo.JPEG"))
    assert not is_supported_media(Path("notes.txt"))


def test_timestamp_filename_format() -> None:
    """
    verify timestamps contain filename safe separators
        :returns: nothing
    """
    assert sanitize_timestamp_filename(datetime(2026, 8, 22, 9, 5, 3)) == "2026-08-22 09_05_03"


def test_build_target_path_organizes_media_by_date(tmp_path: Path) -> None:
    """
    verify organized media receives a date folder and timestamp name
    :param tmp_path: temporary destination directory
        :returns: nothing
    """
    value = datetime(2026, 8, 22, 9, 5, 3)
    result = build_target_path(
        tmp_path, Path("photo.JPG"), Path("album/photo.JPG"), set(),
        True, True, True, True, value,
    )
    assert result == tmp_path / "2026-08-22" / "2026-08-22 09_05_03.JPG"


def test_build_target_path_avoids_existing_and_reserved_names(tmp_path: Path) -> None:
    """
    verify destination naming never overwrites a collision
    :param tmp_path: temporary destination directory
        :returns: nothing
    """
    (tmp_path / "file.txt").write_text("existing", encoding="utf-8")
    used = {tmp_path / "file_1.txt"}
    result = build_target_path(
        tmp_path, Path("file.txt"), Path("file.txt"), used,
        False, True, True, True,
    )
    assert result == tmp_path / "file_2.txt"
