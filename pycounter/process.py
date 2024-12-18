from pycounter.models import Stats
from pathlib import Path
import typer


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

    except FileNotFoundError:
        typer.echo(f"File {file_path} not found")


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

    except FileNotFoundError:
        typer.echo(f"File {file_path} not found")
