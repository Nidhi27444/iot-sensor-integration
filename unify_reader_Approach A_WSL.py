import json, csv, time, os
import xml.etree.ElementTree as ET
from datetime import datetime
from pymongo import MongoClient

# MongoDB: no authentication
client = MongoClient("mongodb://localhost:27017/")
db = client["sensor_data"]
collection = db["unified"]

# Paths
BASE_DIR = os.path.dirname(__file__)
FILES_DIR = os.path.join(BASE_DIR, "files")
OUTPUT_FILE = os.path.join(FILES_DIR, "unified_data.json")

def read_txt():
    try:
        path = os.path.join(FILES_DIR, "sensor1.txt")
        with open(path) as f:
            lines = f.read().splitlines()
        return {"sensor": "I2C", "data": lines[1].split(": ")[1]}
    except Exception as e:
        print("TXT read error:", e)
        return {}

def read_csv():
    try:
        path = os.path.join(FILES_DIR, "sensor2.csv")
        with open(path) as f:
            reader = csv.DictReader(f)
            return {"sensor": "SPI", "data": next(reader)}
    except Exception as e:
        print("CSV read error:", e)
        return {}

def read_json():
    try:
        path = os.path.join(FILES_DIR, "sensor3.json")
        with open(path) as f:
            return {"sensor": "BLE", "data": json.load(f)}
    except Exception as e:
        print("JSON read error:", e)
        return {}

def read_xml():
    try:
        path = os.path.join(FILES_DIR, "sensor4.xml")
        tree = ET.parse(path)
        root = tree.getroot()
        data = {child.tag: child.text for child in root}
        return {"sensor": "WiFi", "data": data}
    except Exception as e:
        print("XML read error:", e)
        return {}

def unify_data():
    timestamp = datetime.now().isoformat()
    return {
        "timestamp": timestamp,
        "sensor1": read_txt(),
        "sensor2": read_csv(),
        "sensor3": read_json(),
        "sensor4": read_xml()
    }

if __name__ == "__main__":
    os.makedirs(FILES_DIR, exist_ok=True)
    while True:
        try:
            data = unify_data()

            # Write to local JSON file
            if os.path.exists(OUTPUT_FILE):
                with open(OUTPUT_FILE, "r") as f:
                    all_data = json.load(f)
            else:
                all_data = []

            all_data.append(data)

            with open(OUTPUT_FILE, "w") as f:
                json.dump(all_data, f, indent=4)

            print("[✓] Updated:", OUTPUT_FILE)

            # Insert into MongoDB
            collection.insert_one(data)
            print("[✓] Inserted into MongoDB")

        except Exception as e:
            print("[✗] Error:", e)

        time.sleep(5)
