import pandas as pd
from datetime import datetime

class TariffData:
    def __init__(self):
        self.data = None

    def load_data(self, file):
        try:
            if file.filename.endswith('.csv'):
                self.data = pd.read_csv(file)
            elif file.filename.endswith('.xlsx'):
                self.data = pd.read_excel(file)
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def get_usage_data(self):
        return self.data if self.data is not None else pd.DataFrame()
