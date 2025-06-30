import RPi.GPIO as GPIO

RELAY_PIN = 2 # we're using gpio 2
GPIO.setmode(GPIO.BCM) # use gpio numbers instead of pin numbers
GPIO.setup(RELAY_PIN, GPIO.OUT) # set it to be an output
GPIO.output(RELAY_PIN, GPIO.LOW) # turn it off
GPIO.cleanup() # clean up and exit gracefully
