from rich.table import Table
from rich import box
from pycounter.console import console


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
    # console.save_svg(path="test.svg")
