import argparse
import pkg_resources
from pycounter.__main__ import count


def main(argv: str | None = None) -> int:
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
        version=f"{pkg_resources.get_distribution('pycounter').version}",
    )

    parser.add_argument(
        "-e",
        "--ext",
        help="extension to filter for",
        action="store",
        choices=[".py", ".md"],
        type=str,
    )

    args = parser.parse_args(argv)

    count(args.path, args.ext)


if __name__ == "__main__":
    main()
