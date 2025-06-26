---
title: "The Printer Pi Pro"
author: "Anicetus"
description: "The all-in-one Raspberry Pi 3D printer add-on!"
created_at: "2025-06-26"
---

## total time: 3 hrs

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
