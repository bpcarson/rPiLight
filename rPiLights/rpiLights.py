from Adafruit_IO import MQTTClient
import RPi.GPIO as gp
ADAFRUIT_IO_USERNAME = "UserName"
ADAFRUIT_IO_KEY = "Key"
red = 0;
blue = 0;
# add GPIO pinouts to 
gpios=[11,13,15,16,18,29,31,31]
gp.setwarnings(False)
gp.setmode(gp.BOARD)

for i in range(len(gpios)):
	gp.setup(gpios[i],gp.OUT)




def connected(client):
    client.subscribe('locationlights') # or change to whatever name you used

# this gets called every time a message is received
def message(client, feed_id, payload):
     if payload == "test":
        print("Message test received from IFTTT.")
     elif payload == "Red entered":
     	print("Red is home")
     	if blue == 1:
     		print("light dance")
     		lightDance()
     		print("settle down")
     	red = 1;
     	setLights(red,blue,gpios)
     elif payload == "Blue entered":
     	print("Blue is home")
     	if red == 1:
     		print("light dance")
     		lightDance()
     		print("settle down")
     	blue=1;
     	setLights(red,blue,gpios)
     elif payload == "Red exited":
        print("Red left home")
        red = 0;
        setLights(red,blue,gpios)
     elif payload == "Blue exited":
        print("Blue left home")
        blue = 0;
        setLights(red,blue,gpios)
     elif payload == "Bedtime":
        print("Shutting down...")
        print("Shutdown dance")
     elif payload == "Wakeup":
        print("Powering up")
        print("Light dance")
        lightDance()
        print("Check last input from stream")
     else:
        print("Message from IFTTT: %s" , payload)

def lightdance():
	# light up blue/red lights in succession with dimming/brightening of white lights
	# 
	gpios= [11,13,15,16,18,29,31,31]; # gpios
	white= 32 # white gpio
	for i in range(10000):
		gp.output(white,gp.HIGH)
		for j in range(8):
			gp.output(gpios[j],gp.HIGH)
			pause(j*i*10)
		pause(i*5)
		


def setLights(red,blue,gpios):
	#red gpios
	Rgpio = [11,13,15,16];
	if red == 1:
		for i in range(len(Rgpio)):
			gp.output(Rgpio[i],gp.HIGH)
	else:
		for i in range(len(Rgpio)):
			gp.output(Rgpio[i],gp.LOW)
	#blue gpios
	Bgpio = [18,29,31,31];
	if blue == 1:
		for i in range(len(Bgpio)):
			gp.output(Bgpio[i],gp.HIGH)
	else:
		for i in range(len(Bgpio)):
			gp.output(Bgpio[i],gp.LOW)
	#white lights
	if red == 1 or blue == 1:
		white=1;
	else:
		white=0;



client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_message    = message 

client.connect()

client.loop_blocking() # block forever on client loop  