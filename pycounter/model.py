from pathlib import Path
from rich.table import Table
from rich import box
from rich.console import Console


console = Console(record=True)


def create_table(stats: dict, title: str, **kwargs) -> None:
    """Create and print a rich table

    Args:
        stats (dict): dictionary of values to display
        title (str): Title or table
    """
    if console.is_dumb_terminal:
        measure_style = None
        value_style = None
    else:
        measure_style = "cyan"
        value_style = "green"

    table = Table(title=title, box=box.ASCII, **kwargs)

    table.add_column("Measure", justify="right", style=measure_style, no_wrap=True)
    table.add_column("Value", style=value_style)

    for k, v in stats.items():
        if k == "net_lines":
            table.add_section()
        if k == "net_files":
            table.add_section()
        table.add_row(k, v)

    console.print(table)
    console.line(1)


def find_files(path: str | Path, ext: str | None) -> list[Path]:
    """Find files based on extension. Automatically filters out .git folders and files

    Args:
        path (str | Path): Path to search in
        ext (str | None): File extension to search for

    Returns:
        list[Path]: list of file paths as Path objects
    """
    files = Path(path).rglob("*")
    # Filter for files and ignore any .hidden files or folders
    files_filtered = [
        f
        for f in files
        if f.is_file() and not any(part.startswith(".") for part in f.parts)
    ]

    if ext:
        return [f for f in files_filtered if ext == f.suffix]
    return files_filtered


def create_file_summary(files: list[Path]) -> dict:
    """Create a dictionary of file counts by type for each path

    Args:
        files (list[Path]): list of Path objects

    Returns:
        dict: Dictionary with keys for file type and values of counts
    """

    files_hash: dict[str, int] = dict()
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
