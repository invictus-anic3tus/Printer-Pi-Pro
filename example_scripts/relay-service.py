import RPi.GPIO as GPIO
import time
import signal
import sys

RELAY_PIN = 2 # we're using GPIO 2

def cleanup(sig, frame)
    GPIO.cleanup() # this sets everything low, turning off the relay
    sys.exit(0) # exits with success

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH) # switch the relay on

signal.signal(signal.SIGINT, cleanup) # this handles Ctrl+C's and other interruptions
signal.signal(signal.SIGTERM, cleanup) # this handles systemd's termination signals

while True: # this doesn't let the script turn off until it's interrupted or ended
    time.sleep(1) # wait for one second between loops, so as not to overload the system lol
