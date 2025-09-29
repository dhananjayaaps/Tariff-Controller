from flask import Flask, request, jsonify
from config.config import Config
from services.tariff_calculator import TariffCalculator
import os

app = Flask(__name__)
app.config.from_object(Config)
calculator = TariffCalculator()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        if calculator.tariff_data.load_data(file):
            return jsonify({"message": "File uploaded successfully"}), 200
        return jsonify({"error": "Invalid file format or data"}), 400
    return jsonify({"error": "Unsupported file format"}), 400

@app.route('/calculate_bill', methods=['POST'])
def calculate_bill():
    tariff_type = request.json.get('tariff_type')
    if not tariff_type or tariff_type not in calculator.tariff_configs:
        return jsonify({"error": "Invalid or missing tariff type"}), 400

    try:
        if tariff_type == "flat":
            total_kwh = calculator.tariff_data.get_usage_data()['kWh'].sum()
            bill = calculator.calculate_flat_bill(total_kwh)
            return jsonify({"bill": bill, "breakdown": {"total_kwh": total_kwh, "rate": calculator.tariff_configs["flat"]["rate"], "fixed_fee": calculator.tariff_configs["flat"]["fixed_fee"]}})
        elif tariff_type == "tou":
            bill, breakdown = calculator.calculate_tou_bill()
            return jsonify({"bill": bill, "breakdown": breakdown})
        elif tariff_type == "tiered":
            bill, breakdown = calculator.calculate_tiered_bill()
            return jsonify({"bill": bill, "breakdown": breakdown})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/compare_tariffs', methods=['GET'])
def compare_tariffs():
    try:
        results, cheapest = calculator.compare_tariffs()
        return jsonify({"comparison": results, "cheapest": cheapest})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/get_usage_trend', methods=['GET'])
def get_usage_trend():
    try:
        data = calculator.tariff_data.get_usage_data()
        if data.empty:
            return jsonify({"error": "No data available"}), 400
        trend = [{"timestamp": str(row['timestamp']), "kWh": row['kWh']} for _, row in data.iterrows()]
        return jsonify({"trend": trend}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update_tariff', methods=['POST'])
def update_tariff():
    tariff_type = request.json.get('tariff_type')
    if not tariff_type or tariff_type not in calculator.tariff_configs:
        return jsonify({"error": "Invalid tariff type"}), 400
    config = request.json.get('config')
    if not config:
        return jsonify({"error": "No configuration provided"}), 400
    try:
        if tariff_type == "flat":
            calculator.tariff_configs["flat"]["rate"] = float(config.get("rate", 0.25))
            calculator.tariff_configs["flat"]["fixed_fee"] = float(config.get("fixed_fee", 10))
        elif tariff_type == "tou":
            calculator.tariff_configs["tou"]["peak_rate"] = float(config.get("peak_rate", 0.40))
            calculator.tariff_configs["tou"]["shoulder_rate"] = float(config.get("shoulder_rate", 0.25))
            calculator.tariff_configs["tou"]["offpeak_rate"] = float(config.get("offpeak_rate", 0.15))
            calculator.tariff_configs["tou"]["fixed_fee"] = float(config.get("fixed_fee", 10))
        elif tariff_type == "tiered":
            tiers = [(float(t[0]), float(t[1])) for t in config.get("tiers", [(100, 0.20), (300, 0.30), (float('inf'), 0.40)])]
            calculator.tariff_configs["tiered"]["tiers"] = tiers
            calculator.tariff_configs["tiered"]["fixed_fee"] = float(config.get("fixed_fee", 10))
        return jsonify({"message": f"{tariff_type} tariff updated", "config": calculator.tariff_configs[tariff_type]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
