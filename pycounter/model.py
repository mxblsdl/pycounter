from pycounter.classes import Stats
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
    files = [f for f in files if f.is_file() and not f.parts[0].startswith(".")]
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


def process_py_file(file_path: str, stats: Stats) -> None:
    """Count different attributes in a python file

    Args:
        file_path (str): path to file
        stats (Stats): Stats object to record attributes
    """
    try:
        with open(file_path, "r") as file:
            stats.add("number_files")
            DOCSTRING_FLAG = False

            if Path(file_path).stat().st_size == 0:
                stats.add("empty_files")

            for line in file:
                if line.strip() == "" and not DOCSTRING_FLAG:
                    stats.add("blank_lines")
                    continue

                if '"""' in line.split():
                    if line.split()[0] == '"""':
                        stats.add("docstring_lines")
                        DOCSTRING_FLAG = not DOCSTRING_FLAG
                        continue

                if DOCSTRING_FLAG:
                    stats.add("docstring_lines")
                    continue

                if line.startswith("import"):
                    stats.add("import_lines")
                    continue

                if line.startswith("from") and "import" in line.split():
                    stats.add("import_lines")
                    continue

                if line.strip()[0] == "#":
                    stats.add("comment_lines")
                    continue

                stats.total_lines += 1

    except FileNotFoundError as e:
        console.print(f"File {file_path} not found")
        console.print_exception(e, word_wrap=True)


def process_md_file(file_path: str, stats: Stats) -> None:
    """Count different attributes in a markdown file

    Args:
        file_path (str): Path to file
        stats (Stats): Stats object to record attributes
    """
    try:
        with open(file_path, "r") as file:
            stats.add("number_files")

            if Path(file_path).stat().st_size == 0:
                stats.add("empty_files")

            for line in file:
                if line.strip() == "":
                    stats.add("blank_lines")
                    continue

                if line.startswith("#"):
                    switch = {
                        1: "h_one_lines",
                        2: "h_two_lines",
                        3: "h_three_lines",
                        4: "h_four_lines",
                    }
                    heading_type = switch.get(line.count("#"))

                    stats.add(heading_type)

                stats.total_lines += 1

    except FileNotFoundError as e:
        console.print(f"File {file_path} not found")
        console.print_exception(e, word_wrap=True)
