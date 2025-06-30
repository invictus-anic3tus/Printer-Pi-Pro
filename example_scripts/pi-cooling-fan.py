import RPi.GPIO as GPIO
import time
from gpiozero import CPUTemperature # make sure to install gpiozero if it isn't already

FAN_PIN = 18 # we're using GPIO 18
FREQ = 25000  # 25khz PWM frequency makes the fan smooth

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

pwm = GPIO.PWM(FAN_PIN, FREQ)
pwm.start(0)  # Start with fan off

cpu = CPUTemperature()
temp = cpu.temperature # grab cpu temp

def cleanup(sig, frame)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup() # this sets everything low, turning off the relay
    sys.exit(0) # exits with success

signal.signal(signal.SIGINT, cleanup) # this handles Ctrl+C's and other interruptions
signal.signal(signal.SIGTERM, cleanup) # this handles systemd's termination signals

try:
  while True:
    temp = cpu.temperature # update temp reading
    if temp < 30: # 30°C or less
      pwm.ChangeDutyCycle(0)
    elif temp < 40: # 30°-40°
      pwm.ChangeDutyCycle(25)
    elif temp < 50: # 40°-50°
      pwm.ChangeDutyCycle(50)
    else: # 50°+
      pwm.ChangeDutyCycle(100)
  
    time.sleep(2) # wait two seconds to not consume CPU (and make temp go up!)
except KeyboardInterrupt:
  print("Keyboard interrupt received")
finally:
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
  
