from pathlib import Path

import pytest

from mover_git.core import FileEntry, human_size, make_batches, make_commit_message, validate_paths


def entry(name: str, size: int) -> FileEntry:
    """
    create a file entry for deterministic tests
    :param name: file name for the entry
    :param size: file size in bytes
    :returns: constructed file entry
    """
    path = Path(name)
    return FileEntry(path, path, size)


def test_make_batches_honors_limit_and_order() -> None:
    """
    verify batches stay within the configured limit
        :returns: nothing
    """
    batches = make_batches([entry("a", 6), entry("b", 4), entry("c", 1)], limit=10)
    assert [[item.rel_path.name for item in batch] for batch in batches] == [["a", "b"], ["c"]]


def test_make_batches_skips_individual_file_above_limit() -> None:
    """
    verify files larger than a batch are excluded
        :returns: nothing
    """
    assert make_batches([entry("large", 11), entry("small", 2)], limit=10) == [[entry("small", 2)]]


@pytest.mark.parametrize(
    ("size", "formatted"),
    [(0, "0.00 B"), (1024, "1.00 KB"), (1024**2 * 2, "2.00 MB")],
)
def test_human_size(size: int, formatted: str) -> None:
    """
    verify byte counts use binary units
    :param size: byte count to format
    :param formatted: expected display value
        :returns: nothing
    """
    assert human_size(size) == formatted


def test_validate_paths_accepts_repository_subfolder(tmp_path: Path) -> None:
    """
    verify a separate source and repository target are accepted
    :param tmp_path: temporary test directory
        :returns: nothing
    """
    source = tmp_path / "source"
    repo = tmp_path / "repo"
    source.mkdir()
    (repo / ".git").mkdir(parents=True)
    assert validate_paths(source, repo, "uploads") == (
        source.resolve(), repo.resolve(), (repo / "uploads").resolve()
    )


def test_validate_paths_rejects_nested_source(tmp_path: Path) -> None:
    """
    verify a source inside the destination is rejected
    :param tmp_path: temporary test directory
        :returns: nothing
    """
    repo = tmp_path / "repo"
    source = repo / "source"
    (repo / ".git").mkdir(parents=True)
    source.mkdir()
    with pytest.raises(ValueError, match="source folder"):
        validate_paths(source, repo)


def test_make_commit_message_adds_later_batch_number() -> None:
    """
    verify commit messages include details and later batch numbers
        :returns: nothing
    """
    result = make_commit_message("archive", 2, 3, 4, 1024, "[01][02][2026] [03:04:05]")
    assert result == "[01][02][2026] [03:04:05] archive 2 - 4 files - 1.00 KB"
