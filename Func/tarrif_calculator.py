import pandas as pd
from io import StringIO
from datetime import datetime

# Constants for tariff configs
FLAT_RATE = 0.25
FLAT_FIXED_FEE = 10
TOU_PEAK_HOURS = [(18, 21)]
TOU_OFFPEAK_CONDITION = 21
TOU_PEAK_RATE = 0.40
TOU_SHOULDER_RATE = 0.25
TOU_OFFPEAK_RATE = 0.15
TOU_FIXED_FEE = 10
TIERED_TIERS = [(100, 0.20), (300, 0.30), (float('inf'), 0.40)]
TIERED_FIXED_FEE = 10

class TariffData:
    def __init__(self):
        self.data = pd.DataFrame()

    def load_from_csv(self, csv_content):
        self.data = pd.read_csv(StringIO(csv_content), parse_dates=['timestamp'])

    def get_usage_data(self):
        return self.data

class TariffCalculator:
    def __init__(self):
        self.tariff_data = TariffData()

    def calculate_flat_bill(self, total_kwh):
        if total_kwh < 0:
            raise ValueError("Total kWh cannot be negative")
        return total_kwh * FLAT_RATE + FLAT_FIXED_FEE

    def determine_tou_category(self, hour):
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23")
        for start, end in TOU_PEAK_HOURS:
            if start <= hour <= end:
                return 'peak'
        if TOU_OFFPEAK_CONDITION < hour or hour < 7:
            return 'off-peak'
        return 'shoulder'

    def calculate_tou_bill(self):
        data = self.tariff_data.get_usage_data()
        if data.empty:
            raise ValueError("No usage data available")
        total_cost = 0.0
        breakdown = {'peak': 0, 'shoulder': 0, 'offpeak': 0}
        for _, row in data.iterrows():
            hour = row['timestamp'].hour
            kwh = row['kWh']
            if kwh < 0:
                raise ValueError("kWh cannot be negative")
            category = self.determine_tou_category(hour)
            if category == 'peak':
                cost = kwh * TOU_PEAK_RATE
                total_cost += cost
                breakdown['peak'] += cost
            elif category == 'shoulder':
                cost = kwh * TOU_SHOULDER_RATE
                total_cost += cost
                breakdown['shoulder'] += cost
            else:
                cost = kwh * TOU_OFFPEAK_RATE
                total_cost += cost
                breakdown['offpeak'] += cost
        return total_cost + TOU_FIXED_FEE, breakdown

    def calculate_tiered_bill(self):
        data = self.tariff_data.get_usage_data()
        if data.empty:
            raise ValueError("No usage data available")
        total_kwh = data['kWh'].sum()
        if total_kwh < 0:
            raise ValueError("Total kWh cannot be negative")
        total_cost = 0.0
        remaining = total_kwh
        prev_threshold = 0.0
        breakdown = {}
        for threshold, rate in TIERED_TIERS:
            if remaining <= 0:
                break
            block = min(remaining, threshold - prev_threshold)
            cost = block * rate
            total_cost += cost
            if block > 0:
                key = f"{int(prev_threshold)}-{int(threshold) if threshold != float('inf') else 'inf'}"
                breakdown[key] = cost
            remaining -= block
            prev_threshold = threshold
        return total_cost + TIERED_FIXED_FEE, breakdown

    def compare_tariffs(self):
        if self.tariff_data.get_usage_data().empty:
            raise ValueError("No usage data available")
        results = {}
        total_kwh = self.tariff_data.get_usage_data()['kWh'].sum()
        results["flat"] = {"bill": self.calculate_flat_bill(total_kwh), "breakdown": None}
        bill, breakdown = self.calculate_tou_bill()
        results["tou"] = {"bill": bill, "breakdown": breakdown}
        bill, breakdown = self.calculate_tiered_bill()
        results["tiered"] = {"bill": bill, "breakdown": breakdown}
        cheapest = min(results, key=lambda x: results[x]["bill"])
        return results, cheapest