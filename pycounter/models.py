from dataclasses import dataclass

@dataclass
class Stats:
    number_files: int = 0
    empty_files: int = 0
    lines: int = 0
    comments: int = 0
    doc_strings: int = 0
    imports: int = 0
    blank_lines: int = 0

    def add(self, var: str, value: int = 1):
        if hasattr(self, var):
            current_value = getattr(self, var)
            setattr(self, var, value + current_value)
            self.lines += 1  # always add one line
        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {var}")