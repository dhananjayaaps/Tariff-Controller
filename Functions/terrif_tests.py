import unittest
import pandas as pd
from tariff_calculator import TariffCalculator
import math

class TestTariffCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = TariffCalculator()

    # Tests for update_flat_config (no return, parameters)
    def test_update_flat_config_positive(self):
        # Positive: Valid inputs
        self.calc.update_flat_config(0.30, 15)
        self.assertEqual(self.calc.tariff_configs["flat"]["rate"], 0.30)
        self.assertEqual(self.calc.tariff_configs["flat"]["fixed_fee"], 15)

    def test_update_flat_config_negative_invalid_rate(self):
        # Negative: Invalid rate (negative)
        with self.assertRaises(ValueError):
            self.calc.update_flat_config(-0.30, 10)

    # Tests for update_tou_config (no return, parameters)
    def test_update_tou_config_positive(self):
        # Positive: Valid inputs
        self.calc.update_tou_config([[17, 21]], 0.45, 0.30, 0.20, 12)
        self.assertEqual(self.calc.tariff_configs["tou"]["peak_hours"], [(17, 21)])
        self.assertEqual(self.calc.tariff_configs["tou"]["peak_rate"], 0.45)
        self.assertEqual(self.calc.tariff_configs["tou"]["fixed_fee"], 12)

    def test_update_tou_config_negative_invalid_hours(self):
        # Negative: Invalid peak hours (end before start)
        with self.assertRaises(ValueError):
            self.calc.update_tou_config([[21, 17]], 0.40, 0.25, 0.15, 10)

    # Tests for update_tiered_config (no return, parameters)
    def test_update_tiered_config_positive(self):
        # Positive: Valid tiers
        self.calc.update_tiered_config([[150, 0.25], [400, 0.35], [math.inf, 0.45]], 20)
        self.assertEqual(self.calc.tariff_configs["tiered"]["tiers"], [(150.0, 0.25), (400.0, 0.35), (math.inf, 0.45)])
        self.assertEqual(self.calc.tariff_configs["tiered"]["fixed_fee"], 20)

    def test_update_tiered_config_negative_invalid_rate(self):
        # Negative: Invalid rate (negative)
        with self.assertRaises(ValueError):
            self.calc.update_tiered_config([[100, -0.20], [300, 0.30]], 10)

    # Tests for calculate_flat_bill (parameters, return value)
    def test_calculate_flat_bill_positive(self):
        # Positive: Standard calculation
        self.assertEqual(self.calc.calculate_flat_bill(300), 85.0)

    def test_calculate_flat_bill_zero(self):
        # Edge case: Zero consumption
        self.assertEqual(self.calc.calculate_flat_bill(0), 10.0)

    def test_calculate_flat_bill_negative(self):
        # Negative case: Invalid input
        with self.assertRaises(ValueError):
            self.calc.calculate_flat_bill(-100)

    # Tests for determine_tou_category (parameters, return value, if-else structure)
    def test_determine_tou_category_peak(self):
        # Positive: Peak hour
        self.assertEqual(self.calc.determine_tou_category(19), 'peak')

    def test_determine_tou_category_offpeak_overnight(self):
        # Positive: Off-peak overnight
        self.assertEqual(self.calc.determine_tou_category(23), 'off-peak')

    def test_determine_tou_category_offpeak_early(self):
        # Positive: Off-peak early morning (covers wrap-around)
        self.assertEqual(self.calc.determine_tou_category(5), 'off-peak')

    def test_determine_tou_category_shoulder(self):
        # Positive: Shoulder hour
        self.assertEqual(self.calc.determine_tou_category(12), 'shoulder')

    def test_determine_tou_category_invalid_low(self):
        # Negative: Invalid hour low
        with self.assertRaises(ValueError):
            self.calc.determine_tou_category(-1)

    def test_determine_tou_category_invalid_high(self):
        # Negative: Invalid hour high
        with self.assertRaises(ValueError):
            self.calc.determine_tou_category(24)

    # Tests for calculate_tou_bill (parameters, return value, if-else via category)
    def test_calculate_tou_bill_positive(self):
        # Positive: Mixed categories
        data = pd.DataFrame({
            'timestamp': pd.to_datetime(['2025-01-01 19:00:00', '2025-01-01 12:00:00', '2025-01-01 23:00:00']),
            'kWh': [100, 120, 80]
        })
        self.calc.tariff_data.data = data
        bill, breakdown = self.calc.calculate_tou_bill()
        self.assertEqual(bill, 92.0)
        self.assertEqual(breakdown['peak'], 40.0)
        self.assertEqual(breakdown['shoulder'], 30.0)
        self.assertEqual(breakdown['offpeak'], 12.0)

    def test_calculate_tou_bill_no_data(self):
        # Edge: No data
        self.calc.tariff_data.data = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.calc.calculate_tou_bill()

    def test_calculate_tou_bill_negative_kwh(self):
        # Negative: Invalid kWh
        data = pd.DataFrame({
            'timestamp': pd.to_datetime(['2025-01-01 19:00:00']),
            'kWh': [-100]
        })
        self.calc.tariff_data.data = data
        with self.assertRaises(ValueError):
            self.calc.calculate_tou_bill()

    # Tests for calculate_tiered_bill (parameters, return value, loop with conditions)
    def test_calculate_tiered_bill_positive(self):
        # Positive: Across tiers
        data = pd.DataFrame({'timestamp': [pd.to_datetime('2025-01-01 00:00:00')] * 350, 'kWh': [1] * 350})
        self.calc.tariff_data.data = data
        bill, breakdown = self.calc.calculate_tiered_bill()
        self.assertEqual(bill, 110.0)
        self.assertEqual(breakdown['0-100'], 20.0)
        self.assertEqual(breakdown['100-300'], 60.0)
        self.assertEqual(breakdown['300-inf'], 20.0)

    def test_calculate_tiered_bill_within_first_tier(self):
        # Positive: Within first tier
        data = pd.DataFrame({'timestamp': [pd.to_datetime('2025-01-01 00:00:00')] * 50, 'kWh': [1] * 50})
        self.calc.tariff_data.data = data
        bill, breakdown = self.calc.calculate_tiered_bill()
        self.assertEqual(bill, 20.0)
        self.assertEqual(breakdown['0-100'], 10.0)

    def test_calculate_tiered_bill_zero_consumption(self):
        # Edge: Zero consumption
        data = pd.DataFrame({'timestamp': [pd.to_datetime('2025-01-01 00:00:00')], 'kWh': [0]})
        self.calc.tariff_data.data = data
        bill, breakdown = self.calc.calculate_tiered_bill()
        self.assertEqual(bill, 10.0)
        self.assertEqual(breakdown, {})

    def test_calculate_tiered_bill_negative(self):
        # Negative: Invalid total
        data = pd.DataFrame({'timestamp': [pd.to_datetime('2025-01-01 00:00:00')], 'kWh': [-50]})
        self.calc.tariff_data.data = data
        with self.assertRaises(ValueError):
            self.calc.calculate_tiered_bill()

    def test_calculate_tiered_bill_no_data(self):
        # Edge: No data
        self.calc.tariff_data.data = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.calc.calculate_tiered_bill()

if __name__ == '__main__':
    unittest.main()