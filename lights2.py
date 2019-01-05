from Adafruit_IO import MQTTClient
from gpiozero import LEDBoard
import time 
ADAFRUIT_IO_USERNAME = "bcarson"
ADAFRUIT_IO_KEY = "6068e9b7a6854ae7bf14bc58196bd691"
global red, blue, leds

# add GPIO pinouts to
leds = LEDBoard(red=LEDBoard(4,5,6,22,27,17), blue = LEDBoard(16,26,13,24,23), white = LEDBoard(25))
leds.off()

def connected(client):
    client.subscribe('locationlights') # or change to whatever name you used

# this gets called every time a message is received
def message(client, feed_id, payload):
     if payload == "test":
        print("Message test received from IFTTT.")
     elif payload == "Red entered":
     	print("Red is home")
     	leds.red.on()
     	print("done lighting")
     elif payload == "Blue entered":
     	print("Blue is home")
     	leds.blue.on()
     	print("done lighting")
     elif payload == "Red exited":
        print("Red left home")
        leds.red.off()
     elif payload == "Blue exited":
        print("Blue left home")
        leds.blue.off()
        print("done lighting")
     elif payload == "Bedtime":
        print("Shutting down...")
        print("Shutdown dance")
        leds.off()
     elif payload == "Wakeup":
        print("Powering up")
        print("Light dance")
        lightdance(leds)
        leds.white.on()
        print("Check last input from stream")
     else:
        print("Message from IFTTT: %s" , payload)

def lightdance(leds):
	# light up blue/red lights in succession with dimming/brightening of white lights
	#
    for led in leds.red:
        led.blink()
        time.sleep(.3)
        
    for led in leds.blue:
        led.blink()
        time.sleep(.3)

    leds.white.on()
    time.sleep(5)
		

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_message    = message 

client.connect()
client.publish('locationlights', "Wakeup")
client.loop_blocking() # block forever on client loop  
