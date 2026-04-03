import json


class JsonParser:
    def __init__(self, file_name: str):
        self._file_name = file_name

    def read(self):
        file_data = None

        with open(self._file_name) as file:
            file_data = json.load(file)

        return file_data
