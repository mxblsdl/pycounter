import argparse
from importlib.metadata import version
from pycounter.__main__ import count
from argparse import Namespace


def main(argv: str | None = None):
    """
    Tool for summarizing

    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The arguments passed on the command line.

    Returns
    -------
    int
        Exit code for the process: if metadata was stripped,
        this will be 1 to stop a commit as a pre-commit hook.
    """
    parser = argparse.ArgumentParser(
        prog="count",
        description="Provide Summary stats for your python files",
        epilog="Built with python",
    )

    parser.add_argument(
        "path",
        nargs="*",
        help="Folder path to process. (default: %(default)s)",
        default="./",
        type=str,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{version('pycounter')}",
    )

    parser.add_argument(
        "-e",
        "--ext",
        help="extension to filter for",
        action="store",
        choices=[".py", ".md", "py", "md"],
        type=str,
    )

    parser.add_argument(
        "--tui",
        help="Launch interactive TUI",
        action="store_true",
    )

    args: Namespace = parser.parse_args(argv)

    if args.tui:
        from pycounter.tui import CounterApp

        app = CounterApp()
        app.run()
    else:
        count(args.path, args.ext)


if __name__ == "__main__":
    main()
