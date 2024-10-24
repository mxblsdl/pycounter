from dataclasses import dataclass, asdict


@dataclass
class Stats:
    number_files: int = 0
    empty_files: int = 0
    net_files: int = 0

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
    heading_one: int = 0
    heading_two: int = 0
    heading_three: int = 0
    heading_four: int = 0



@dataclass
class Py_Stats(Stats):
    total_lines: int = 0
    comment_lines: int = 0
    docstring_lines: int = 0
    import_lines: int = 0
    blank_lines: int = 0
    net_lines: int = 0

    def calc_lines(self):
        self.net_lines = (
            self.total_lines
            - self.comment_lines
            - self.docstring_lines
            - self.import_lines
            - self.blank_lines
        )
