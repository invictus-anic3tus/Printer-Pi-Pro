# Printer-Pi-Pro
The all-in-one Raspberry Pi hat for controlling your 3D printer!

The Printer Pi Pro is a Raspberry Pi hat plus a relay module. The hat controls things like servos, an accelerometer, a fan for cooling the pi, and more. It also controls a relay that can turn your printer on or off!

## What you need:
1. A raspberry pi (duh) with Klipper or Octoprint installed (all features are compatible with both!)
2. The Printer Pi Pro PCB

If you aren't controlling anything with the PCB, that's all you need! However, you likely won't just make the PCB solely to put it on the Pi and not plug anything into it. So here's what you can do with it:

## Features:
1. Onboard passive buzzer: can create little tunes and jingles when your print starts, finishes, cancels, or anything else you want!
2. 5V Fan port: for active cooling your Raspberry Pi. You can code this to turn on when the Pi starts getting hot.
3. Two servo ports: perfect for pitch and yaw of a webcam! or anything else really
4. ADXL345 port: for an accelerometer and input shaping!
5. Relay port: to control an AC or DC relay. This can be for lights, or to turn on/off the printer. More on this later.


How to play music with the buzzer: [https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/9](https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/9)
