from __future__ import annotations

from plyer import filechooser


def open_file() -> bytes | None:
    path = filechooser.open_file(title="Pick a file..")

    if path and isinstance(path, list):
        with open(path[0], "rb") as text_file:
            result = text_file.read()
            return result
    else:
        return None



def save_file(data: str | bytes, path="hash.txt") -> None:
    file_path = filechooser.save_file(title="Save to file..", path=path)

    if file_path:
        if isinstance(file_path, list):
            file_path = file_path[0]
            if type(data) is str:
                with open(file_path, "w") as file:
                    file.write(data)
            elif type(data) in {bytes, bytearray}:
                with open(file_path, "wb") as file:
                    file.write(data)
            else:
                print("nothing", type(data))
        else:
            raise FileNotFoundError
