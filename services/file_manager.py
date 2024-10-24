from __future__ import annotations

from plyer import filechooser


def open_file() -> str | None:
    path = filechooser.open_file(title="Pick a file..")

    if path and isinstance(path, list):
        with open(path[0], "rb") as text_file:
            result = text_file.read()
            return result
    else:
        return None



def save_file(data: str) -> None:
    file_path = filechooser.save_file(title="Save to file..", path="hash.txt")

    if file_path:
        if isinstance(file_path, list):
            file_path = file_path[0]
            with open(file_path, "wb") as file:
                file.write(bytearray(data))
        else:
            raise FileNotFoundError
