from tarrif_calculator import TariffCalculator 
import pandas as pd

def run_tests():
    # Test 1: calculate_flat_bill
    calc = TariffCalculator()
    # Positive: normal consumption
    assert abs(calc.calculate_flat_bill(300) - 85.0) < 1e-10, "Failed positive test for calculate_flat_bill (300 kWh)"
    # Positive: zero consumption
    assert abs(calc.calculate_flat_bill(0) - 10.0) < 1e-10, "Failed positive test for calculate_flat_bill (0 kWh)"
    # Negative: negative consumption
    try:
        calc.calculate_flat_bill(-1)
        assert False, "Should have raised ValueError for negative kWh"
    except ValueError as e:
        assert str(e) == "Total kWh cannot be negative", "Unexpected error message"

    # Test 2: determine_tou_category
    # Positive: peak hour
    assert calc.determine_tou_category(19) == 'peak', "Failed peak category test"
    # Positive: shoulder hour
    assert calc.determine_tou_category(12) == 'shoulder', "Failed shoulder category test"
    # Positive: off-peak hours
    assert calc.determine_tou_category(23) == 'off-peak', "Failed off-peak category test (23)"
    assert calc.determine_tou_category(3) == 'off-peak', "Failed off-peak category test (3)"
    # Positive: boundary cases
    assert calc.determine_tou_category(7) == 'shoulder', "Failed shoulder boundary test (7)"
    assert calc.determine_tou_category(17) == 'shoulder', "Failed shoulder boundary test (17)"
    assert calc.determine_tou_category(18) == 'peak', "Failed peak boundary test (18)"
    assert calc.determine_tou_category(21) == 'peak', "Failed peak boundary test (21)"
    assert calc.determine_tou_category(22) == 'off-peak', "Failed off-peak boundary test (22)"
    assert calc.determine_tou_category(0) == 'off-peak', "Failed off-peak boundary test (0)"
    # Negative: invalid hours
    try:
        calc.determine_tou_category(-1)
        assert False, "Should have raised ValueError for hour -1"
    except ValueError as e:
        assert str(e) == "Hour must be between 0 and 23", "Unexpected error message"
    try:
        calc.determine_tou_category(24)
        assert False, "Should have raised ValueError for hour 24"
    except ValueError as e:
        assert str(e) == "Hour must be between 0 and 23", "Unexpected error message"

    # Test 3: calculate_tou_bill (positive and negative cases)
    # Positive: with mixed categories
    positive_csv = """timestamp,kWh
2025-01-01 12:00:00,1.0
2025-01-01 19:00:00,2.0
2025-01-01 23:00:00,3.0
"""
    calc.tariff_data.load_from_csv(positive_csv)
    bill, breakdown = calc.calculate_tou_bill()
    assert abs(bill - 11.5) < 1e-10, "Failed positive test for calculate_tou_bill bill amount"
    assert abs(breakdown['peak'] - 0.8) < 1e-10, "Failed breakdown peak"
    assert abs(breakdown['shoulder'] - 0.25) < 1e-10, "Failed breakdown shoulder"
    assert abs(breakdown['offpeak'] - 0.45) < 1e-10, "Failed breakdown offpeak"
    # Positive: only off-peak
    offpeak_csv = """timestamp,kWh
2025-01-01 23:00:00,3.0
"""
    calc.tariff_data.load_from_csv(offpeak_csv)
    bill, breakdown = calc.calculate_tou_bill()
    assert abs(bill - 10.45) < 1e-10, "Failed positive test for off-peak only"
    # Negative: empty data
    calc.tariff_data.data = pd.DataFrame()
    try:
        calc.calculate_tou_bill()
        assert False, "Should have raised ValueError for no usage data"
    except ValueError as e:
        assert str(e) == "No usage data available", "Unexpected error message"
    # Negative: negative kWh in data
    negative_kwh_csv = """timestamp,kWh
2025-01-01 12:00:00,-1.0
"""
    calc.tariff_data.load_from_csv(negative_kwh_csv)
    try:
        calc.calculate_tou_bill()
        assert False, "Should have raised ValueError for negative kWh"
    except ValueError as e:
        assert str(e) == "kWh cannot be negative", "Unexpected error message"

    # Test 4: calculate_tiered_bill (positive and negative cases)
    # Positive: full tiers (350 kWh)
    full_tiers_csv = """timestamp,kWh
2025-01-01 00:00:00,50
2025-01-01 01:00:00,100
2025-01-01 02:00:00,200
"""
    calc.tariff_data.load_from_csv(full_tiers_csv)
    bill, breakdown = calc.calculate_tiered_bill()
    assert abs(bill - 110.0) < 1e-10, "Failed positive test for calculate_tiered_bill (350 kWh)"
    assert abs(breakdown['0-100'] - 20.0) < 1e-10, "Failed breakdown 0-100"
    assert abs(breakdown['100-300'] - 60.0) < 1e-10, "Failed breakdown 100-300"
    assert abs(breakdown['300-inf'] - 20.0) < 1e-10, "Failed breakdown 300-inf"
    # Positive: partial tiers (50 kWh)
    partial_csv = """timestamp,kWh
2025-01-01 00:00:00,50
"""
    calc.tariff_data.load_from_csv(partial_csv)
    bill, breakdown = calc.calculate_tiered_bill()
    assert abs(bill - 20.0) < 1e-10, "Failed positive test for calculate_tiered_bill (50 kWh)"
    assert abs(breakdown['0-100'] - 10.0) < 1e-10, "Failed breakdown for partial tiers"
    # Positive: zero consumption
    zero_csv = """timestamp,kWh
2025-01-01 00:00:00,0
"""
    calc.tariff_data.load_from_csv(zero_csv)
    bill, breakdown = calc.calculate_tiered_bill()
    assert abs(bill - 10.0) < 1e-10, "Failed positive test for calculate_tiered_bill (0 kWh)"
    assert breakdown == {}, "Failed breakdown for zero consumption"
    # Negative: empty data
    calc.tariff_data.data = pd.DataFrame()
    try:
        calc.calculate_tiered_bill()
        assert False, "Should have raised ValueError for no usage data"
    except ValueError as e:
        assert str(e) == "No usage data available", "Unexpected error message"
    # Negative: negative total kWh
    negative_total_csv = """timestamp,kWh
2025-01-01 00:00:00,-10
"""
    calc.tariff_data.load_from_csv(negative_total_csv)
    try:
        calc.calculate_tiered_bill()
        assert False, "Should have raised ValueError for negative total kWh"
    except ValueError as e:
        assert str(e) == "Total kWh cannot be negative", "Unexpected error message"

    # Extra Test: compare_tariffs
    # Positive: with data
    calc.tariff_data.load_from_csv(positive_csv)
    results, cheapest = calc.compare_tariffs()
    assert abs(results["flat"]["bill"] - 11.5) < 1e-10, "Failed flat in compare_tariffs"
    assert abs(results["tou"]["bill"] - 11.5) < 1e-10, "Failed tou in compare_tariffs"
    assert abs(results["tiered"]["bill"] - 11.2) < 1e-10, "Failed tiered in compare_tariffs (6*0.2 +10)"
    assert cheapest == "tiered", "Failed cheapest detection"
    # Negative: empty data
    calc.tariff_data.data = pd.DataFrame()
    try:
        calc.compare_tariffs()
        assert False, "Should have raised ValueError for no usage data"
    except ValueError as e:
        assert str(e) == "No usage data available", "Unexpected error message"

if __name__ == "__main__":
    try:
        run_tests()
        print("All unit tests passed successfully. 100% pass rate achieved.")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"Error during testing: {e}")