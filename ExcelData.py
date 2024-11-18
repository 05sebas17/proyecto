import pandas as pd

class ExcelData:
    _instance = None

    def __new__(cls, file_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.file_path = file_path
            cls._instance.data = pd.read_excel(file_path)
        return cls._instance

    def get_data(self):
        return self.data
