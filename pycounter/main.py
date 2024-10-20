import typer
from pathlib import Path

from typing_extensions import Annotated
from pycounter.models import Stats
from pycounter.table import create_table

# A super cool CLI
app = typer.Typer(
    no_args_is_help=True,
    epilog="Count the lines in your code base",
)


@app.command()
def count(
    path: Annotated[str, typer.Argument()] = "./",
    ext: Annotated[str, typer.Option("--ext", "-e")] = None,
):
    stats = Stats()

    files = find_files(path, ext)

    if not ext:
        file_summary = create_file_summary(files)
        create_table(file_summary, title="File type summary")
        raise typer.Exit(0)

    for file in files:
        # TODO different process func for different extensions
        process_file(file, stats)

    stats.calc_lines()
    stats.calc_files()

    create_table(
        stats.dict("files"),
        title="Files Stats",
        caption="A file count summary",
    )
    create_table(
        stats.dict("lines"),
        title="Lines Stats",
    )


def find_files(path: str, ext: str | None):
    files = Path(path).rglob("*")
    # Filter for files and ignore any .git files or folders
    files = [f for f in files if f.is_file() and ".git" not in f.parts]
    # TODO accept list of ext
    if ext:
        return [f for f in files if ext == f.suffix]
    return files


def process_file(file_path: str, stats: Stats):
    try:
        with open(file_path, "r") as file:
            stats.add("number_files")
            DOCSTRING_FLAG = False

            if Path(file_path).stat().st_size == 0:
                # typer.echo(f"empty file {file.name}")
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


def create_file_summary(files: list[Path]) -> dict:
    files_hash = dict()
    for file in files:
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


if __name__ == "__main__":
    # typer.run(app())
    typer.run(count)
