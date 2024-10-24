import typer
from pathlib import Path

from typing_extensions import Annotated
import pycounter.models
from pycounter.table import create_table
from pycounter.process import process_py_file, process_md_file

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
    files = find_files(path, ext)

    if not ext:
        file_summary = create_file_summary(files)
        create_table(file_summary, title="File type summary")
        raise typer.Exit(0)

    # TODO different process func for different extensions
    # Conditional check for file extension type
    if ext == ".py":
        stats = pycounter.models.Py_Stats()

        for file in files:
            process_py_file(file, stats)
        stats.calc_lines()

    elif ext == ".md":
        # TODO cleaner to put more logic within these if else blocks
        # and not fix things up as much
        stats = pycounter.models.Md_Stats()

        for file in files:
            process_md_file(file, stats)
            create_table(
                stats.dict("heading"),
                title=f"Heading Stats for {ext} files",
            )

    stats.calc_files()

    create_table(
        stats.dict("files"),
        title=f"Stats for {ext} files",
        caption="A file count summary",
    )
    create_table(
        stats.dict("lines"),
        title=f"Lines Stats for {ext} files",
    )


def find_files(path: str, ext: str | None) -> str:
    files = Path(path).rglob("*")
    # Filter for files and ignore any .git files or folders
    files = [f for f in files if f.is_file() and ".git" not in f.parts]
    if ext:
        return [f for f in files if ext == f.suffix]
    return files


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
    count("../", ".md")
