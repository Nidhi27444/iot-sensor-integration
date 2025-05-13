import machine
import time
import network
import urequests
import sdcard
import uos
import json

# I2C Setup for MPU6050
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
sensor1_address = 0x68  # MPU6050 I2C address

# Wake up the MPU6050
try:
    i2c.writeto_mem(sensor1_address, 0x6B, b'\x00')
    print("MPU6050 woken up")
except Exception as e:
    print("Failed to wake up MPU6050:", e)

# Initialize SD card
sdd = machine.SDCard(slot=2, width=1, sck=18, miso=19, mosi=23, cs=5)
vfs = uos.VfsFat(sdd)
uos.mount(vfs, "/sdd")

# Create file for SPI test if missing
try:
    with open("/sdd/test01.txt", "x") as file:
        file.write("Hello, SD World!\r\n")
except OSError:
    pass

# WiFi Setup
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("Wokwi-GUEST", "")
while not sta.isconnected():
    time.sleep(1)
print("Connected to WiFi")

# Timestamp formatter
def get_timestamp():
    t = time.localtime()
    return f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

# Read I2C (MPU6050)
def read_i2c_sensor():
    try:
        data = i2c.readfrom_mem(sensor1_address, 0x41, 2)
        raw_temp = (data[0] << 8) | data[1]
        if raw_temp & 0x8000:
            raw_temp -= 0x10000
        temp = (raw_temp / 340.0) + 36.53

        with open("/sdd/sensor1_temp.txt", "a") as file:
            file.write(f"Temp: {temp:.2f}C at {get_timestamp()} \n")

        return {
            "sensor": "I2C - MPU6050",
            "temperature_c": round(temp, 2),
            "timestamp": get_timestamp()
        }
    except Exception as e:
        return {"sensor": "I2C - MPU6050", "error": str(e)}

# Read SPI (SD file content)
def read_spi_sensor():
    try:
        with open("/sdd/test01.txt", "r") as file:
            sensor2_data = file.read().strip()

        with open("/sdd/sensor2_data.csv", "a") as file:
            file.write(f"{get_timestamp()},{sensor2_data}\n")

        return {
            "sensor": "SPI - SD Card",
            "value": sensor2_data,
            "timestamp": get_timestamp()
        }
    except Exception as e:
        return {"sensor": "SPI - SD Card", "error": str(e)}

# Read WiFi (public IP)
def read_wifi_sensor():
    try:
        response = urequests.get("http://httpbin.org/get")
        data = response.json()
        ip = data.get('origin', 'Unknown')

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sensor4>
    <timestamp>{get_timestamp()}</timestamp>
    <origin>{ip}</origin>
</sensor4>
"""
        with open("/sdd/sensor4_data.xml", "a") as file:
            file.write(xml_content)

        return {
            "sensor": "WiFi - Public IP",
            "ip": ip,
            "timestamp": get_timestamp()
        }
    except Exception as e:
        return {"sensor": "WiFi - Public IP", "error": str(e)}

# Main loop
while True:
    sensor1 = read_i2c_sensor()
    sensor2 = read_spi_sensor()
    sensor4 = read_wifi_sensor()

    result = {
        "timestamp": get_timestamp(),
        "sensor_1": sensor1,
        "sensor_2": sensor2,
        "sensor_4": sensor4
    }

    print(json.dumps(result))
    time.sleep(5)
