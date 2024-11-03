import typer

from typing_extensions import Annotated
from pycounter.models import Md_Stats, Py_Stats
from pycounter.table import create_table
from pycounter.process import process_py_file, process_md_file
from pycounter.console import console
from pycounter.helpers import find_files, create_file_summary

app = typer.Typer(
    no_args_is_help=True,
    epilog="Count the lines in your code base",
)


@app.command()
def count(
    path: Annotated[str, typer.Argument(help="Path to search")] = "./",
    ext: Annotated[
        str,
        typer.Option("--ext", "-e", help="File extension to calculate stas for"),
    ] = None,
):
    if ext and ext[0] != ".":
        ext = "." + ext

    files = find_files(path, ext)

    if not ext:
        file_summary = create_file_summary(files)

        create_table(file_summary, title="File type summary")
        raise typer.Exit(0)

    # Conditional check for file extension type
    if ext == ".py":
        stats = Py_Stats()

        for file in files:
            process_py_file(file, stats)
        stats.calc_lines()
        stats.calc_files()

    elif ext == ".md":
        stats = Md_Stats()

        for file in files:
            process_md_file(file, stats)
        stats.calc_files()
    else:
        console.print(f"Supplied file extension {ext} not currently supported")
        raise typer.Exit(0)

    create_table(
        stats.dict("files"),
        title=f"Stats for {ext} files",
        caption="A file count summary",
    )
    create_table(
        stats.dict("lines"),
        title=f"Lines Stats for {ext} files",
    )


if __name__ == "__main__":
    count("../")
