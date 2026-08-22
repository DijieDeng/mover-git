from pathlib import Path

from mover_git.git import normalize_github_url, parse_status_paths, repo_relative_paths


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
