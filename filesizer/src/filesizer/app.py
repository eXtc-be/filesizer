"""
a tool to list files, largest first
"""


import toga
from toga.style.pack import COLUMN, ROW

from pathlib import Path


def get_file_list(folder: Path) -> list[tuple[[Path, int]]]:
    files = []
    print(folder.absolute())

    for file in folder.rglob('*'):
        print(file.as_posix())
        if file.is_file():
            files.append((file, file.stat().st_size, ))

    return sorted(files, key=lambda x: x[1], reverse=True)


class FileSizer(toga.App):
    def startup(self):
        main_box = toga.Box(direction=COLUMN)

        self.path_input = toga.TextInput(flex=1, value=Path(__file__).parent.as_posix())

        go_button = toga.Button(
            'GO',
            on_press=self.list_files,
            margin=5,
        )

        path_box = toga.Box(direction=ROW, margin=5)
        path_box.add(self.path_input)
        path_box.add(go_button)
        main_box.add(path_box)

        file_box = toga.Box(direction=COLUMN, margin=5, flex=1)
        self.file_list = toga.Table(
            columns=['size', 'path'],
            flex=1,
        )
        file_box.add(self.file_list)
        main_box.add(file_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def list_files(self, widget):
        self.file_list.data = [
            (f'{file[1]:15,}', file[0].absolute())
            for file in get_file_list(Path(self.path_input.value))
        ]


def main():
    return FileSizer()
