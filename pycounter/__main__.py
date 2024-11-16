from pycounter.classes import Md_Stats, Py_Stats
from pycounter.model import (
    create_file_summary,
    find_files,
    process_md_file,
    process_py_file,
    create_table,
    console,
)


def count(
    path: str,
    ext: str,
):
    if ext and ext[0] != ".":
        ext = "." + ext

    files = find_files(path, ext)

    if not ext:
        file_summary = create_file_summary(files)

        create_table(file_summary, title="File type summary")
        raise exit(0)

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
        raise exit(0)

    create_table(
        stats.dict("files"),
        title=f"Stats for {ext} files",
        caption="A file count summary",
    )
    create_table(
        stats.dict("lines"),
        title=f"Lines Stats for {ext} files",
    )
