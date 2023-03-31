#  GNU nano 5.4                               TEST2.py                                         
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

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
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

# Subprograms
def temp():
    return "   %.1f C" % (sensor.data.temperature)

def humi():
    return "  %.1f %%" % (sensor.data.humidity)

def pres():
    return "  %.f hPa" % (sensor.data.pressure)

def gas():
    return " %.f Ohms" % (sensor.data.gas_resistance)

# Main program
while True:
    sensor.get_sensor_data()
    
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "MINISENSOR", fill="white", font=FontTemp)

        draw.text((4, 30), "TEMP:  ", fill="white", font=FontTemp2)
        draw.text((42, 30), temp(), fill="white", font=FontTemp2)
        
        draw.text((5, 45), "HUM: ", fill="white", font=FontTemp2)
        draw.text((42, 45), humi(), fill="white", font=FontTemp2)

        draw.text((5, 65), "PRES:  ", fill="white", font=FontTemp2)
        draw.text((42,65), pres(), fill="white", font=FontTemp2)

        draw.text((5, 85), "GAS:  ", fill="white", font=FontTemp2)
        draw.text((10, 100), gas(), fill="white", font=FontTemp2)
        
    time.sleep(1)

