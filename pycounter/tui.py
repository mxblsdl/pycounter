import logging
import subprocess
from textual.app import ComposeResult, App
from textual.containers import Container
from textual.widgets import (
    Header,
    Footer,
    Button,
    Static,
    RadioButton,
    Input,
    RadioSet,
)

logging.basicConfig(
    level=logging.DEBUG,
    filename="/tmp/pycounter_tui.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class CounterApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Input(
                placeholder="Click 'Browse' to select a directory",
                id="path_input",
                disabled=True,
            ),
            # DirectoryTree("./", id="directory_tree"),
            Button("Browse", id="browse_btn"),
            Static("Extension:", id="ext_label"),
            RadioSet(
                RadioButton(".py", id="ext_py", value=True),
                RadioButton(".md", id="ext_md"),
                RadioButton("All", id="ext_all"),
                id="extension_radio_set",
            ),
            Button("Count Files", id="count_btn"),
            Static(id="output"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "browse_btn":
            try:
                result = subprocess.run(
                    ["zenity", "--file-selection", "--directory"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    selected_path = result.stdout.strip()
                    self.query_one("#path_input", Input).value = selected_path
                    logging.debug(f"Selected directory: {selected_path}")
            except FileNotFoundError:
                self.query_one("#output", Static).update(
                    "Zenity is not installed. Please install it to use the directory browser."
                )
        elif event.button.id == "count_btn":
            directory = self.query_one("#path_input", Input)
            path = directory.value
            logging.debug(f"Selected directory: {path}")
            radio_set = self.query_one("#extension_radio_set", RadioSet)
            selected_radio = radio_set.pressed_button

            if selected_radio is None:
                self.query_one("#output", Static).update(
                    "Please select a file extension."
                )
                return
            # Get the selected extension
            if selected_radio.id == "ext_py":
                ext = ".py"
            elif selected_radio.id == "ext_md":
                ext = ".md"
            else:
                ext = None  # All files

            # Call your count function here
            self.query_one("#output", Static).update(
                f"Counting {ext or 'all'} files in {path}..."
            )


if __name__ == "__main__":
    app = CounterApp()
    app.run()
