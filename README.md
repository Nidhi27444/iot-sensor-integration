
# 🔗 IoT Sensor Integration System – WSL + ESP32 (Scalable Prototype)

This repository includes two integrated components for scalable IoT sensor monitoring:

1. **WSL-based Python Simulation** – for local file-based sensor simulation, unification, and MongoDB logging
2. **ESP32 (MicroPython/Wokwi)** – for real-time sensor interaction with I2C, SPI, and Wi-Fi modules

---

## 📦 Architecture Overview

- Modular sensor data ingestion (via file or hardware)
- Unified JSON formatting for all sensor types
- Scalable thread-safe design for up to 40 sensors
- MongoDB integration for centralized storage
- Designed for simulation and real hardware deployment

---

## 🧪 WSL/Python Simulation (Software Layer)

### ✅ Implemented

- Reads `.txt`, `.csv`, `.json`, `.xml` files
- Converts to unified format
- Basic error handling
- MongoDB batch insert support

### 🚧 Planned

- `threading.Thread` per sensor
- `threading.Lock` for safe access
- Heartbeat + failure recovery
- Auto-scaling config for 40+ sensors

---

## 🔌 ESP32/Wokwi Simulation (Hardware Layer)

### ✅ Implemented

- I2C-based MPU6050 sensor
- SPI-based SD card logging
- Wi-Fi setup
- Loop-based sensor polling
- Basic error handling (`try/except`)

### 🚧 Planned

- BLE sensor integration
- Heartbeat monitor per sensor
- GPIO-based power cycling
- MQTT/HTTP data uploads

---

## 🔁 Scaling Strategy

| Layer          | Strategy                          |
|----------------|-----------------------------------|
| Threads        | Use ThreadPool or asyncio         |
| DB Access      | Locking + Semaphore + Batching    |
| Failure Detection | Heartbeat dict + logs         |
| Expansion      | I2C mux, multiple ESP32s or GPIO  |

---

## 🛠 How to Run

### WSL:
```bash
pip install pymongo
python unify_reader.py
```

### ESP32 (Wokwi):
1. Open in https://wokwi.com
2. Load `main.py`, `sdcard.py`, `diagram.json`
3. Connect I2C and SPI sensors virtually
4. View logs in Serial Monitor

---

## 📁 Project Structure

```
iot_sensor_project/
├── unify_reader.py
├── sensor1.txt / .csv / .json / .xml


iot_sensor_wokwi_Project/
├── main.py
├── sdcard.py
├── diagram.json
├── wokwi-project.txt

```

---

## 📍 Conclusion

This project demonstrates a reliable, extensible, and modular sensor architecture for both software simulation and hardware testing. It’s structured for continuous improvement with future goals of full automation, fault tolerance, and large-scale IoT integration.

