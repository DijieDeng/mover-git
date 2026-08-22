from pathlib import Path
from urllib.parse import urlparse


def normalize_github_url(remote_url: str) -> str | None:
    """
    convert a Git remote URL into a GitHub web address
    :param remote_url: git remote URL
    :returns: normalized GitHub URL or None
    """
    remote_url = remote_url.strip()
    if remote_url.startswith("git@github.com:"):
        path = remote_url.split(":", 1)[1]
    elif remote_url.startswith(("https://", "http://", "ssh://")):
        parsed = urlparse(remote_url)
        if parsed.hostname != "github.com":
            return None
        path = parsed.path.lstrip("/")
    else:
        return None
    return f"https://github.com/{path.removesuffix('.git').rstrip('/')}"


def parse_status_paths(status: str) -> list[str]:
    """
    parse paths from Git porcelain status output
    :param status: porcelain version one status output
    :returns: changed repository relative paths
    """
    paths = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path.strip('"'))
    return paths


def repo_relative_paths(repo: Path, paths: list[Path]) -> list[str]:
    """
    convert paths into repository relative pathspecs
    :param repo: repository root path
    :param paths: paths inside the repository
    :returns: sorted unique Git pathspecs
    """
    resolved_repo = repo.resolve()
    result = {path.resolve().relative_to(resolved_repo).as_posix() for path in paths}
    return sorted(result)
