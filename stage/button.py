import RPi.GPIO as GPIO
import time
import os

# Set up the GPIO pins
BUTTON_PIN = 17  # Change this if you're using a different GPIO pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Bouton appuyé!")
    os.system("python3 /home/pi/pair_device_dbus.py")  # Path to your Bluetooth pairing script

# Add event detection for the button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("En attente de l'appui sur le bouton...")

try:
    while True:
        time.sleep(0.1)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("Sortie du programme...")
finally:
    GPIO.cleanup()
