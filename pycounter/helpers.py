from pathlib import Path


def find_files(path: str, ext: str | None) -> list[str]:
    """Find files based on extension. Automatically filters out .git folders and files

    Args:
        path (str): Path to search in
        ext (str | None): File extension to search for

    Returns:
        list[str]: list of file paths as strings
    """
    files = Path(path).rglob("*")
    # Filter for files and ignore any .git files or folders
    files = [f for f in files if f.is_file() and ".git" not in f.parts]
    if ext:
        return [f for f in files if ext == f.suffix]
    return files


def create_file_summary(files: list[Path]) -> dict:
    """Create a dictionary of file counts by type for each path

    Args:
        files (list[Path]): list of Path objects

    Returns:
        dict: Dictionary with keys for file type and values of counts
    """

    files_hash = dict()
    for file in files:
        if not isinstance(file, Path):
            continue
        if file.suffix == "":
            key = file.name
        else:
            key = file.suffix
        if key not in files_hash.keys():
            files_hash[key] = 0
        files_hash[key] += 1
    files_hash = dict(
        sorted(files_hash.items(), key=lambda item: item[1], reverse=True)
    )
    return {k: str(v) for k, v in files_hash.items()}
