import socket
import os
import sys
import struct


class SocketServer(object):
    def __init__(self, ip='', port=33333):
        self.ip = ip
        self.port = port
        self.clientSock = None
        self.cliAddr = None
        try:
            self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSock.bind((self.ip, self.port))
            self.serverSock.listen(1)  # this server class only support one connection
        except socket.error as msg:
            print(msg)
            sys.exit(1)

    def __del__(self):
        self.serverSock.close()

    def waitConnection(self):
        print("Wait for Connection.....................")
        self.clientSock, self.cliAddr = self.serverSock.accept()  # addr: tuple(ip,port)
        print("Accept connection from {0}".format(self.cliAddr))  # show (ip:port)
        msg = self.ip + ' has accepted your connection request.'
        b_msg = msg.encode(encoding='utf8')
        self.clientSock.sendall(b_msg)

    def hasConnection(self):
        if self.clientSock is not None:
            return True
        else:
            return False

    def receiveFile(self, savepath='./'):
        if self.clientSock is None:
            print("No connection yet!")
            return
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        if deal_image(self.clientSock, self.cliAddr, savepath):
            msg = self.ip + ' has got your message'
            b_msg = msg.encode(encoding='utf8')
            try:
                self.clientSock.sendall(b_msg)
            except OSError:
                print("Connection lost...")

    def sendFile(self, filepath):
        if self.clientSock is None:
            print("No connection yet!")
            return
        if not os.path.isfile(filepath):
            print(filepath + ' does not exists!')
            return
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)
        try:
            self.clientSock.send(fhead)
            fp = open(filepath, 'rb')
            while True:
                data = fp.read(1024)  # read file data
                if not data:
                    print('\'{0}\' has been sent to ({1}:{2})'.format(filepath, self.cliAddr[0], self.cliAddr[1]))
                    break
                self.clientSock.send(data)  # send file data by binary code
        except OSError:
            print("Connection lost...")

    def receiveMessage(self):
        try:
            data = self.clientSock.recv(1024)
            print(data)
        except OSError:
            pass


def sock_receive():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 33333))
        s.listen(1)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.....................")

    while True:
        sock, addr = s.accept()  # addr: tuple(ip,port)
        print("Accept connection from {0}".format(addr))  # show (ip:port)
        deal_image(sock, addr)


def deal_image(sock, addr, savepath='./'):
    received = False
    while True:
        try:
            fileinfo_size = struct.calcsize('128sq')
            buf = sock.recv(fileinfo_size)
            if buf:
                filename, filesize = struct.unpack('128sq', buf)
                fn = filename.decode().strip('\x00')
                fn = os.path.basename(fn)
                new_filename = os.path.join(savepath, fn)

                recvd_size = 0
                fp = open(new_filename, 'wb')

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = sock.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = sock.recv(1024)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                print("\'{0}\' received.".format(fn))
                received = True
            sock.close()
            break
        except OSError:
            return False
    return received


if __name__ == '__main__':
    server = SocketServer()
    server.waitConnection()
    server.sendFile('../UHD.png')
    while True:
        # server.receiveMessage()
        server.receiveFile('serverSaved')
