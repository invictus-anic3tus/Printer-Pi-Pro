---
title: "The Printer Pi Pro"
author: "Anicetus"
description: "The all-in-one Raspberry Pi 3D printer add-on!"
created_at: "2025-06-26"
---

## total time: 5.5 hrs

# firstly

i want to thank everybody at hack club who's making this possible. if you don't know, hack club is a 100% 501(c)(3) nonprofit run by zach latta + friends made for coders and electronics peoples 18 and under. this project is made possible through their highway to undercity program, where teens are empowered to build their dreams with up to $350 in funding!

so a big thank you out to acon, alex ren, cyao, ducc, bunnyguy, phthallo, paolo, kareem, rhys, kl, ian, tongyu, manitej, cinders, and m0hid!!

## i'm anicetus
if you're reading this on hack club, you may very well already know me. but if you dont, here's a bit of info:
1. I live in the usa
2. i'm ok at coding
3. but i think im pretty good at electronics and stuff!
4. i've designed (most of) a custom keyboard
5. and a custom 3d printer

so yeah i've got a bit to put on my resume! but anyways let's get down to business.

# log

### Day one - june 26
So i want to make this for the raspberry pi running my homemade 3D printer. right now if my printer is off, i have to be physically there to turn it on, and that's no fun! Additionally, if i'm away from home and will be for a while, I'd want to be able to turn the PSU and mainboard and stuff off while it's idle. So I thought to meself, "well now, how would i be able to turn on or off my 3d printer with just the interface on me raspberry pi?"

I did a tad bit of research, and found out the answer was simple: a relay! I simply connect the relay to the AC power going to my PSU, and the raspberry pi can turn it on or off. however, those relays take a good amount of amperage to work, and the raspberry pi's gpio pins don't exactly give that much. so, we need a transistor circuit to be able to switch 5V from the main power supply to power the relay! nice!

then i though to meself: "why stop at just controlling a relay? as long as i'm making this thing, i could control other things as well!" turns out the transistor circuit from before is perfect for running a two-pin 5V fan. easy enough. i also wanna power servos, an adxl345 accelerometer (input shaping!) and maybe some other peripherals.

I started making the PCB, and got the schematic done and the footprints added. I had to do a bunch of research about solid state relay amperage, raspberry pi pwm outputs, servos, and more to get started. i also added a buzzer, hopefully to make music and little beeps!

3 hrs

### day two - june 27
Today i pretty much finished the PCB! I placed all the components (all on one side for single-side assembly!), routed the wires, and learned how to do copper pours. I added some ground pours both cuz they're cool and because it makes it easy to route ground. It's looking quite good!

![image](https://github.com/user-attachments/assets/212c6bb1-469b-4982-8ee0-1dbfafb7e7b5)
![image](https://github.com/user-attachments/assets/ec7b4a88-47f5-4b49-b34a-9a16911ebaaf)

![image](https://github.com/user-attachments/assets/40646067-8858-459c-b2b9-70f6d47fd802)
![image](https://github.com/user-attachments/assets/e3e629e5-3b6e-499d-bef0-8d23540b7ec5)

R2D2!  
![image](https://github.com/user-attachments/assets/57d79acc-35de-48f9-ad8a-6c532dd3ad10)

I think i want to manufacture it green to match the Rpi. Right now, the PCB uses the two transistor circuits to control the fan and the relay (and i realized you can actually control any 5V device with it that uses less than 800mA), two PWM gpios to control servos, a gpio to control the buzzer, and SPI communication to the ADXL345 port. I made a ton of progress today, which I'm proud of.

2.5 hrs

### day three - june 28
today i plan to finish this thing! It's a pretty simple and small project, but i'm happy im able to make pcbs this quickly now. I did a bit of factchecking and realized I need the buzzer on a PWM pin, not just any old GPIO. I unrouted it, fixed the schematic, deleted my copper pours, _re-_routed it, and finally redid my copper pours. perfect! I've been making this thing in easyeda instead of kicad, because I used it once on a computer without Kicad and thought it'd be nice to learn another eda program. turns out, it's actually super... well... easy!

However, I realized that I can't export kicad files (which everybody uses) from easyeda... welp. I can, however, export Altium files! I think KiCad can import those. According to EasyEDA, sometimes Altium exports come out wrong. So if you need to import it into Altium or KiCad, know that you may need to do some patchwork. Here's some pics for reference: (ignore the giant copyright :yum:)

![Printer-Pi-Pro_Schematic_Reference](https://github.com/user-attachments/assets/ad8f5136-f840-4789-8cb4-63b0acfed138)
