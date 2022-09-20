from calc import mod2div
from err_gen import err_gen
from configuration import *
import socket

class Client :

    def __init__(self, ipadd, portn) :
        
        self.socket_ = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_.connect((ipadd, portn))

    def asciiToBin(self, data) :
        # ascii to bin.

        return bin(int.from_bytes(data.encode(), 'big'))

    def appendZero(self, message) :
        # append n - 1 0's.
        message = (message.ljust(len(CRC_GENERATOR) - 1 + len(message), '0'))
        return message

    def encode(self, data) :

        # convert ascii to bin 
        message = self.asciiToBin(data)
        divident = self.appendZero(message)
        
        # generate and append crc
        crc = mod2div(divident, CRC_GENERATOR)
        curr_frame = (message + crc)

        return curr_frame


    def send_file(self, filename = 'file.txt'):
        
        f = open(filename)
        data = f.read(FRAME_SIZE)

        while len(data) > 0:
            
            # encode data
            curr_frame = self.encode(data)

            # induce error
            curr_frame = err_gen().induce_err(curr_frame)

            # send frame
            self.socket_.send(curr_frame.encode())
            
            # receive acknowledgement
            if self.socket_.recv(BUFFER_SIZE).decode() == 'OK':
                data = f.read(FRAME_SIZE)
        
        # Terminate session
        self.socket_.send(END_OF_FILE.encode())
        self.socket_.close()
        f.close()
        print("File sent")


newclient = Client(ipadd="127.0.0.1", portn=3241)
newclient.send_file(filename="file.txt")
