import typer
from pathlib import Path

from typing_extensions import Annotated
from pycounter.models import Stats

# A super cool CLI
app = typer.Typer(
    no_args_is_help=True,
    epilog="Count the lines in your code base",
)


@app.command()
def count(
    path: Annotated[str, typer.Argument()] = "./",
    ext: Annotated[str, typer.Option("--ext", "-e")] = ".py",
):
    stats = Stats()

    files = find_files(path, ext)

    for file in files:
        process_file(file, stats)

    typer.echo(stats)


def find_files(path: str, ext: str):
    files = Path(path).rglob("*")
    # Filter for files and ignore any .git files or folders
    files = [f for f in files if f.is_file() and ".git" not in f.parts]
    # TODO accept list of ext
    return [f for f in files if ext == f.suffix]


def process_file(file_path: str, stats: Stats):
    try:
        with open(file_path, "r") as file:
            stats.add("number_files")
            DOCSTRING_FLAG = False

            if Path(file_path).stat().st_size == 0:
                typer.echo(f"empty file {file.name}")
                stats.add("empty_files")

            for line in file:
                if line == "\n" and not DOCSTRING_FLAG:
                    stats.add("blank_lines")
                    continue

                if '"""' in line.split():
                    if line.split()[0] == '"""':
                        stats.add("doc_strings")
                        DOCSTRING_FLAG = not DOCSTRING_FLAG
                        continue

                if DOCSTRING_FLAG:
                    stats.add("doc_strings")
                    continue

                if line.startswith("import"):
                    stats.add("imports")
                    continue

                if line.startswith("from") and "import" in line.split():
                    stats.add("imports")
                    continue

                if line.strip()[0] == "#":
                    stats.add("comments")
                    continue

                stats.lines += 1

    except FileNotFoundError:
        typer.echo(f"File {file_path} not found")


# if __name__ == "__main__":
# typer.run(app())
#     typer.run(count)
