from models.tariff import TariffData

class TariffCalculator:
    def __init__(self):
        self.tariff_data = TariffData()
        self.tariff_configs = {
            "flat": {"rate": 0.25, "fixed_fee": 10},
            "tou": {"peak_rate": 0.40, "shoulder_rate": 0.25, "offpeak_rate": 0.15, "fixed_fee": 10},
            "tiered": {"tiers": [(100, 0.20), (300, 0.30), (float('inf'), 0.40)], "fixed_fee": 10}
        }

    def calculate_flat_bill(self, total_kwh):
        if total_kwh < 0:
            raise ValueError("Total kWh cannot be negative")
        config = self.tariff_configs["flat"]
        return total_kwh * config["rate"] + config["fixed_fee"]

    def determine_tou_category(self, hour):
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23")
        if 18 <= hour <= 22:
            return 'peak'
        elif 22 < hour or hour < 7:
            return 'off-peak'
        else:
            return 'shoulder'

    def calculate_tou_bill(self):
        data = self.tariff_data.get_usage_data()
        if data.empty:
            raise ValueError("No usage data available")
        usages = [(row['timestamp'].hour, row['kWh']) for _, row in data.iterrows()]
        config = self.tariff_configs["tou"]
        total_cost = 0.0
        for hour, kwh in usages:
            if kwh < 0:
                raise ValueError("kWh cannot be negative")
            category = self.determine_tou_category(hour)
            if category == 'peak':
                total_cost += kwh * config["peak_rate"]
            elif category == 'shoulder':
                total_cost += kwh * config["shoulder_rate"]
            else:
                total_cost += kwh * config["offpeak_rate"]
        return total_cost + config["fixed_fee"], {
            'peak': sum(kwh for h, kwh in usages if self.determine_tou_category(h) == 'peak') * config["peak_rate"],
            'shoulder': sum(kwh for h, kwh in usages if self.determine_tou_category(h) == 'shoulder') * config["shoulder_rate"],
            'offpeak': sum(kwh for h, kwh in usages if self.determine_tou_category(h) == 'off-peak') * config["offpeak_rate"]
        }

    def calculate_tiered_bill(self):
        data = self.tariff_data.get_usage_data()
        if data.empty:
            raise ValueError("No usage data available")
        total_kwh = data['kWh'].sum()
        if total_kwh < 0:
            raise ValueError("Total kWh cannot be negative")
        config = self.tariff_configs["tiered"]
        total_cost = 0.0
        remaining = total_kwh
        prev_threshold = 0.0
        breakdown = {}
        for threshold, rate in config["tiers"]:
            if remaining <= 0:
                break
            block = min(remaining, threshold - prev_threshold)
            total_cost += block * rate
            if block > 0:
                breakdown[f"{prev_threshold}-{threshold if threshold != float('inf') else 'inf'}"] = block * rate
            remaining -= block
            prev_threshold = threshold
        return total_cost + config["fixed_fee"], breakdown

    def compare_tariffs(self):
        results = {}
        for tariff in self.tariff_configs:
            if tariff == "flat":
                total_kwh = self.tariff_data.get_usage_data()['kWh'].sum()
                results[tariff] = {"bill": self.calculate_flat_bill(total_kwh), "breakdown": None}
            elif tariff == "tou":
                bill, breakdown = self.calculate_tou_bill()
                results[tariff] = {"bill": bill, "breakdown": breakdown}
            elif tariff == "tiered":
                bill, breakdown = self.calculate_tiered_bill()
                results[tariff] = {"bill": bill, "breakdown": breakdown}
        cheapest = min(results.items(), key=lambda x: x[1]["bill"]) if results else None
        return results, cheapest[0] if cheapest else None