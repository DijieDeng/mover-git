from pathlib import Path

from mover_git.git import (
    normalize_github_url,
    parse_status_paths,
    repo_relative_paths,
    validate_destination_repo,
)


def test_normalize_github_urls() -> None:
    """
    verify common GitHub remote formats become browser links
        :returns: nothing
    """
    expected = "https://github.com/quangshuynh/mover-git"
    assert normalize_github_url("git@github.com:quangshuynh/mover-git.git") == expected
    assert normalize_github_url("https://github.com/quangshuynh/mover-git.git") == expected
    assert normalize_github_url("https://example.com/repo.git") is None


def test_parse_status_paths_handles_rename() -> None:
    """
    verify porcelain status parsing returns changed paths
        :returns: nothing
    """
    assert parse_status_paths(" M old.txt\nR  before.txt -> after.txt\n?? new.txt") == [
        "old.txt", "after.txt", "new.txt"
    ]


def test_repo_relative_paths_are_sorted_and_unique(tmp_path: Path) -> None:
    """
    verify staging pathspecs are repository relative
    :param tmp_path: temporary repository directory
        :returns: nothing
    """
    paths = [tmp_path / "b.txt", tmp_path / "folder" / "a.txt", tmp_path / "b.txt"]
    assert repo_relative_paths(tmp_path, paths) == ["b.txt", "folder/a.txt"]


def test_validate_destination_repo_accepts_valid_repo(tmp_path: Path) -> None:
    """
    verify a valid Git repository passes validation
    :param tmp_path: temporary directory fixture
        :returns: nothing
    """
    repo = tmp_path / "valid-repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    resolved = validate_destination_repo(repo)
    assert resolved == repo.resolve()


def test_validate_destination_repo_rejects_nonexistent(tmp_path: Path) -> None:
    """
    verify a missing destination raises a clear error
    :param tmp_path: temporary directory fixture
        :returns: nothing
    """
    missing = tmp_path / "does-not-exist"
    try:
        validate_destination_repo(missing)
        assert False, "expected ValueError for nonexistent destination"
    except ValueError as exc:
        assert "does not exist" in str(exc)
        assert str(missing) in str(exc)


def test_validate_destination_repo_rejects_non_directory(tmp_path: Path) -> None:
    """
    verify a file path (not a directory) raises a clear error
    :param tmp_path: temporary directory fixture
        :returns: nothing
    """
    file_path = tmp_path / "not-a-dir.txt"
    file_path.write_text("hello")
    try:
        validate_destination_repo(file_path)
        assert False, "expected ValueError for non-directory destination"
    except ValueError as exc:
        assert "not a directory" in str(exc)
        assert str(file_path) in str(exc)


def test_validate_destination_repo_rejects_non_git_directory(tmp_path: Path) -> None:
    """
    verify a directory without .git raises a clear error
    :param tmp_path: temporary directory fixture
        :returns: nothing
    """
    plain_dir = tmp_path / "plain-folder"
    plain_dir.mkdir()
    try:
        validate_destination_repo(plain_dir)
        assert False, "expected ValueError for non-Git directory"
    except ValueError as exc:
        assert "not a Git repository" in str(exc)
        assert str(plain_dir) in str(exc)
