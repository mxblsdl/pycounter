from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Stats:
    number_files: int = 0
    empty_files: int = 0
    net_files: int = 0
    total_lines: int = 0

    def add(self, var: str, value: int = 1):
        if hasattr(self, var):
            current_value = getattr(self, var)
            setattr(self, var, value + current_value)
            self.total_lines += 1  # always add one line
        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {var}")

    def calc_files(self):
        self.net_files = self.number_files - self.empty_files

    def dict(self, type: str):
        return {k: str(v) for k, v in asdict(self).items() if type in k}


@dataclass
class Md_Stats(Stats):
    total_lines: int = 0
    blank_lines: int = 0
    h_one_lines: int = 0
    h_two_lines: int = 0
    h_three_lines: int = 0
    h_four_lines: int = 0

    def process_md_file(self, file_path: str | Path) -> None:
        """Count different attributes in a markdown file

        Args:
            file_path (str | Path): Path to file
        """
        try:
            with open(file_path, "r") as file:
                self.add("number_files")

                if Path(file_path).stat().st_size == 0:
                    self.add("empty_files")

                for line in file:
                    if line.strip() == "":
                        self.add("blank_lines")
                        continue

                    if line.startswith("#"):
                        switch = {
                            1: "h_one_lines",
                            2: "h_two_lines",
                            3: "h_three_lines",
                            4: "h_four_lines",
                        }
                        heading_type = switch.get(line.count("#"))
                        if heading_type:
                            self.add(heading_type)

                    self.total_lines += 1

        except FileNotFoundError as e:
            print(f"File {file_path} not found: {e}")


@dataclass
class Py_Stats(Stats):
    total_lines: int = 0
    comment_lines: int = 0
    docstring_lines: int = 0
    import_lines: int = 0
    blank_lines: int = 0
    net_lines: int = 0

    def calc_lines(self):
        """Calculate net lines of code by subtracting comment, docstring, import and blank lines from total lines"""
        self.net_lines = (
            self.total_lines
            - self.comment_lines
            - self.docstring_lines
            - self.import_lines
            - self.blank_lines
        )

    def process_py_file(self, file_path: str | Path) -> None:
        """Count different attributes in a python file

        Args:
            file_path (str | Path): path to file
        """
        try:
            with open(file_path, "r") as file:
                self.add("number_files")
                DOCSTRING_FLAG = False

                if Path(file_path).stat().st_size == 0:
                    self.add("empty_files")

                for line in file:
                    line = line.strip()
                    if line == "" and not DOCSTRING_FLAG:
                        self.add("blank_lines")
                        continue

                    if '"""' in line.split():
                        if line.split()[0] == '"""':
                            self.add("docstring_lines")
                            DOCSTRING_FLAG = not DOCSTRING_FLAG
                            continue

                    if DOCSTRING_FLAG:
                        self.add("docstring_lines")
                        continue

                    if line.startswith("import"):
                        self.add("import_lines")
                        continue

                    if line.startswith("from") and "import" in line.split():
                        self.add("import_lines")
                        continue

                    if line.startswith("#"):
                        self.add("comment_lines")
                        continue

                    self.add("total_lines")

        except FileNotFoundError as e:
            print(f"File {file_path} not found: {e}")
