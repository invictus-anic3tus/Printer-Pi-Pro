
import RPi.GPIO as GPIO
import time

buzzer_pin = 12

notes = {
    'A': 440.00,
    'B': 493.88,
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00
}

tune = [
    'C',
    'E',
    'G',
    'G',
    'F',
    'D',
    'E',
    'C',
    'C',
    'G',
    'A',
    'G',
    'REST',
    'B'
]

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
pwm = GPIO.PWM(buzzer_pin, 261.63)  # start at the freq for middle C
pwm.start(50)

for note in tune:
    if note == 'REST':
        pwm.ChangeDutyCycle(0)  # temporarily off
    else:
        freq = notes[note]
        pwm.ChangeFrequency(freq)
        pwm.ChangeDutyCycle(50)  # 50% power
    time.sleep(0.5)  # wait for 1/2 second before going to next note

pwm.stop()
GPIO.cleanup()
