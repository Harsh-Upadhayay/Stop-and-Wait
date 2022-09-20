import socket
from calc import mod2div
from configuration import *

class Server :

    def __init__(self, ipaddr, portn) :

        self.socket_ = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_.bind((ipaddr, portn))
        self.socket_.listen(5)


    def iszero(self, data) :
        for x in data :
            if x != '0' :
                return False
        return True


    def isCurrupted(self, message) :
        return not self.iszero(mod2div(message, CRC_GENERATOR))

    
    def decode(self, message) :
        message = message[ : 1 - len(CRC_GENERATOR)]
        n = int(message, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

   
    def log(self, loghandle, itr, received_frame, retrie_count) :
        
        loghandle.write("Frame Number : " + str(itr) + "\n")
        loghandle.write("Frame Content : \"" + self.decode(received_frame) + "\"\n")
        loghandle.write("Retries : " + str(retrie_count) + "\n\n")

    

    def receive_file(self, filepath, logpath) :
        
        received_socket, addr = self.socket_.accept()

        f = open (filepath, 'w')
        l = open (logpath, 'w')
        
        itr = 1
        retrie_count = 0

        while 1:
            
            received_frame = received_socket.recv(BUFFER_SIZE).decode()
            
            if received_frame == END_OF_FILE :
                f.close()
                l.close()
                self.socket_.close()
                print("File Received")
                return
                

            if self.isCurrupted(received_frame) :
                retrie_count += 1
                received_socket.send(REJECT.encode())
            
            else :
                # Received file
                f.write(self.decode(received_frame))

                # Log
                self.log(l, itr, received_frame, retrie_count)

                retrie_count = 0
                received_socket.send(ACCEPT.encode())


newServer = Server(ipaddr="127.0.0.1", portn=3241)
newServer.receive_file(filepath="received_data.txt", logpath="logfile.txt")