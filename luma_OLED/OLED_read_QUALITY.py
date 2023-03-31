#!/usr/bin/env python

import bme680
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont

# Load a larger font
FontTemp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
FontTemp2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

device = sh1106(i2c(port=1, address=0x3C), width=128, height=128, rotate=2)

sensor.data.temperature = 0
sensor.data.pressure = 0
sensor.data.humidity = 0
sensor.data.gas_resistance = 0

# Variables for air quality calculation
burn_in_time = 300
burn_in_data = []
start_time = time.time()
curr_time = time.time()
gas_baseline = 0
hum_baseline = 40.0
hum_weighting = 0.25

# Burn-in period
while curr_time - start_time < burn_in_time:
    curr_time = time.time()
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        burn_in_data.append(gas)
        time.sleep(1)

gas_baseline = sum(burn_in_data[-50:]) / 50.0

# Subprograms
def temp():
    return "   %.1f C" % (sensor.data.temperature)

def humi():
    return "  %.1f %%" % (sensor.data.humidity)

def pres():
    return "  %.f hPa" % (sensor.data.pressure)

def gas():
    return " %.f Ohms" % (sensor.data.gas_resistance)

def calculate_scores(hum_offset, gas_offset, hum_baseline, hum_weighting, gas_baseline):
    if hum_offset > 0:
        hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)
    else:
        hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

    if gas_offset > 0:
        gas_score = (gas / gas_baseline) * (100 - (hum_weighting * 100))
    else:
        gas_score = 100 - (hum_weighting * 100)

    return hum_score, gas_score

# Main program
burn_in_time = 300
start_time = time.time()
curr_time = time.time()

print('Collecting gas resistance burn-in data for 5 mins\n')
while curr_time - start_time < burn_in_time:
    curr_time = time.time()
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        burn_in_data.append(gas)
        print('Gas: {0} Ohms'.format(gas))
        time.sleep(1)

gas_baseline = sum(burn_in_data[-50:]) / 50.0
hum_baseline = 40.0
hum_weighting = 0.25

while True:
    sensor.get_sensor_data()
    if sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        gas_offset = gas_baseline - gas
        hum = sensor.data.humidity
        hum_offset = hum - hum_baseline
        hum_score, gas_score = calculate_scores(hum_offset, gas_offset, hum_baseline, hum_weighting, gas_baseline)
        air_quality_score = hum_score + gas_score
        
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "MINISENSOR", fill="white", font=FontTemp)

        draw.text((4, 30), "TEMP:  ", fill="white", font=FontTemp2)
        draw.text((42, 30), temp(), fill="white", font=FontTemp2)
        
        draw.text((5, 45), "HUM: ", fill="white", font=FontTemp2)
        draw.text((42, 45), humi(), fill="white", font=FontTemp2)

        draw.text((5, 65), "PRES:  ", fill="white", font=FontTemp2)
        draw.text((42, 65), pres(), fill="white", font=FontTemp2)

        draw.text((5, 85), "GAS:  ", fill="white", font=FontTemp2)
        draw.text((42, 85), gas(), fill="white", font=FontTemp2)

        draw.text((90, 85), "IAQ:", fill="white", font=FontTemp2)
        draw.text((105, 100), "{:.1f}".format(air_quality_score), fill="white", font=FontTemp2)

    time.sleep(1)

