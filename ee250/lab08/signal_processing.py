import paho.mqtt.client as mqtt
import time

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 3
ranger1_dist = []
ranger2_dist = []

##########

##########
def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    ranger1_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
	

	
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()
	
	
	MAX_AVERAGE_LIST_LENGTH = 3
	ranger1_average = []
	ranger2_average = []

	#MAX_SLOPE_LIST = 3
	ranger1_slope #= []
	ranger2_slope #= []
	
	side_Max = 60
	
	ranger1_average.append(ranger1_dist[-1:])
	ranger2_average.append(ranger2_dist[-1:])
    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        if(len(ranger1_dist) > 3):
			ranger1_average.append((ranger1_dist[0] + ranger1_dist[1] + ranger1_dist[2] + ranger1_dist[3]) / 3)
			ranger1_average.append((ranger1_dist[0] + ranger1_dist[1] + ranger1_dist[2] + ranger1_dist[3]) / 3)
			ranger1_average = ranger1_average[-MAX_AVERAGE_LIST_LENGTH:]
			
			ranger1_slope = ranger1_average[-2] - ranger1_average[-1]
		
			ranger2_average.append((ranger2_dist[0] + ranger2_dist[1] + ranger2_dist[2] + ranger2_dist[3]) / 3)
			ranger2_average.append((ranger2_dist[0] + ranger2_dist[1] + ranger2_dist[2] + ranger2_dist[3]) / 3)
			ranger2_average = ranger2_average[-MAX_AVERAGE_LIST_LENGTH:]
			
			ranger2_slope = ranger2_average[-2] - ranger2_average[-1]
		
		
			if((ranger1_average > 125) && (ranger2_average > 125)):
				print("No object ") 
				
			else if (ranger1_average[-1:] < side_Max):
				if(ranger1_slope > 0):
					print("Moving left ")
				else	
					print("Standing Right ")
					
			else if (ranger2_average[-1:] < side_Max):
				if(ranger2_slope > 0):
					print("Moving left ")
				else	
					print("Standing Right ")
			else
				print("Middle ")
				
		
        # TODO: detect movement and/or position
		"""if(len(ranger1_dist) >= 10):
			ranger1_slope.append(ranger1_dist[8] - ranger1_dist[9])
			ranger1_slope = ranger1_slope[-MAX_SLOPE_LIST:]
			
			ranger2_slope.append(int(ranger2_dist[8]) - int(ranger2_dist[9]))
			ranger2_slope = ranger2_slope[-MAX_SLOPE_LIST:]
			
			ranger1_average.append((int(ranger1_slope[0])+int(ranger1_slope[1])+int(ranger1_slope[2])+int(ranger1_slope[3])+ int(ranger1_slope[4]))/5)
			ranger1_average = ranger1_average[-MAX_AVERAGE_LIST_LENGTH:]
			
			ranger2_average.append((int(ranger2_slope[0])+int(ranger2_slope[1])+int(ranger2_slope[2])+int(ranger2_slope[3])+ int(ranger2_slope[4]))/5)
			ranger2_average = ranger2_average[-MAX_AVERAGE_LIST_LENGTH:]
				
			print("ranger1_dist: " + str(ranger1_dist[-1:]) + ", ranger2_dist: " + 
				str(ranger2_dist[-1:]) + ", ranger1 slope: " + str(ranger1_slope[-1:]) + ", ranger2 slope: " + str(ranger2_slope[-1:]) +
				", ranger1_average: " + str(ranger1_average[-1:]) + ", ranger1_average: " + str(ranger1_average[-1:])
		else		
			print("ranger1_dist: " + str(ranger1_dist[-1:]) + ", ranger2_dist: " + 
				str(ranger2_dist[-1:]))
			"""
			
			
			
        time.sleep(0.2)
		
		
		
		
		
		
		
		
		
		
		
		
		
		