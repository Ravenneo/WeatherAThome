#  Automartise ON/OFF                                                                   

import os
import signal

# Add this function to handle the script termination
def signal_handler(signum, frame):
    # Clean up the PID file when the script is terminated
    if os.path.exists("weather_OLED.pid"):
        os.remove("weather_OLED.pid")
    exit(0)

# Register the signal handler for SIGTERM and SIGINT
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Create the PID file
with open("weather_OLED.pid", "w") as pid_file:
    pid_file.write(str(os.getpid()))

#This python code shows Temperature, Humedity and preasure from the Bme680 Sensor in the OLED sh1107 screen. 

import bme680
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
# Load a larger font
FontTemp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
FontTemp2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
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

#Uncomment #GAS lines if you want to see Gas_Resistance, but the Gas sensor will warm the termometer making Temp readings more elevated.

#sensor.set_gas_status(bme680.ENABLE_GAS_MEAS) #GAS

#sensor.set_gas_heater_temperature(320) #GAS
#sensor.set_gas_heater_duration(150) #GAS
#sensor.select_gas_heater_profile(0) #GAS

device = sh1106(i2c(port=1, address=0x3C), width=128, height=128, rotate=2)

sensor.data.temperature = 0
sensor.data.pressure = 0
sensor.data.humidity = 0
#sensor.data.gas_resistance = 0 #GAS

# Subprograms
def temp():
    return "   %.1f C" % (sensor.data.temperature -6.1)

def humi():
    return "  %.1f %%" % (sensor.data.humidity + 13.5 ) #I have compared readings from BM680 sensor with and indoor sensor and decided to modify final ridings for temperature and humedity. Maybe my sensor was not propperly working

def pres():
    return "  %.f hPa" % (sensor.data.pressure)

#def gas(): #GAS
#    return " %.f Ohms" % (sensor.data.gas_resistance) #GAS

# Main program
text_position = 0
direction = 1
while True:
    sensor.get_sensor_data()
    
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "MINISENSOR", fill="white", font=FontTemp)

        draw.text((4, 18 + text_position), "TEMP:  ", fill="white", font=FontTemp2)
        draw.text((5, 37 + text_position), temp(), fill="white", font=FontTemp2)

        draw.text((5, 54 + text_position), "HUM: ", fill="white", font=FontTemp2)
        draw.text((5, 69 + text_position), humi(), fill="white", font=FontTemp2)

        draw.text((5, 86 + text_position), "PRES:  ", fill="white", font=FontTemp2)
        draw.text((5, 105 + text_position), pres(), fill="white", font=FontTemp2)

#       draw.text((5, 87), "GAS:  ", fill="white", font=FontTemp2) #GAS
#       draw.text((10, 100), gas(), fill="white", font=FontTemp2) #GAS

        # Update text_position
        text_position += direction
        if text_position > 10 or text_position < 0:
            direction = -direction

    time.sleep(1)
# Remove the PID file when the script exits gracefully
if os.path.exists("weather_OLED.pid"):
    os.remove("weather_OLED.pid")
