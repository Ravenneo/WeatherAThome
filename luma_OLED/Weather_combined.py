import bme680
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
import subprocess  # bring the codes for the RGB matrix

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

device = sh1106(i2c(port=1, address=0x3C), width=128, height=128, rotate=2)

sensor.data.temperature = 0
sensor.data.pressure = 0
sensor.data.humidity = 0

def temp():
    return "   %.1f C" % (sensor.data.temperature - 6.1)

def humi():
    return "  %.1f %%" % (sensor.data.humidity + 13.5)

def pres():
    return "  %.f hPa" % (sensor.data.pressure)

current_range = None
text_position = 0
direction = 1

while True:
    sensor.get_sensor_data()

    temperature = sensor.data.temperature - 6.1
    if temperature < 17:
        subprocess.Popen(["python", "cold.py"])
    elif 17 <= temperature <= 19:
        subprocess.Popen(["python", "medium.py"])
    else:
        subprocess.Popen(["python", "warm.py"])
    
    # rest of your code

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
