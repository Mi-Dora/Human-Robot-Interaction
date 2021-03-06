import socket
import os
import sys
import struct
import time

__all__ = ['sock_send', 'SocketClient']


def sock_send(filepath, ip='116.235.60.223', port=33333):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        # s.connect(('127.0.0.1', 33333))  # For local host test
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                        os.stat(filepath).st_size)
    s.send(fhead)

    fp = open(filepath, 'rb')
    while True:
        data = fp.read(1024)  # read file data
        if not data:
            print('\'{0}\' has been sent to ({1}:{2})'.format(filepath, ip, port))
            break
        s.send(data)  # send file data by binary code
    s.close()


class SocketClient(object):
    def __init__(self, ip='116.235.60.223', port=33333):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     self.sock.connect((self.ip, self.port))
        #     # self.receiveMessage()
        # except socket.error as msg:
        #     print(msg)
        #     print(sys.exit(1))

    def __del__(self):
        self.sock.close()

    def connect(self):
        self.sock.close()
        self.sock = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))

    def sendFile(self, filepath):
        if not os.path.isfile(filepath):
            print(filepath + ' does not exists!')
            return
        self.connect()
        time.sleep(1)
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)
        self.sock.send(fhead)
        time.sleep(1)
        fp = open(filepath, 'rb')
        while True:
            data = fp.read(1024)  # read file data
            if not data:
                print('\'{0}\' has been sent to ({1}:{2})'.format(filepath, self.ip, self.port))
                break
            self.sock.send(data)  # send file data by binary code

    def receiveFile(self, savepath='./'):
        received = False
        fn = None
        self.connect()
        try:
            # print('Waiting for receiving')
            fileinfo_size = struct.calcsize('128sq')
            buf = self.sock.recv(fileinfo_size)
            if buf:
                filename, filesize = struct.unpack('128sq', buf)
                fn = filename.decode().strip('\x00')
                fn = os.path.basename(fn)
                new_filename = os.path.join(savepath, fn)
                if not os.path.exists(savepath):
                    os.mkdir(savepath)
                recvd_size = 0
                fp = open(new_filename, 'wb')

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = self.sock.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = self.sock.recv(1024)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                received = True
                print("\'{0}\' received.".format(fn))
                # if received:
                #     msg = 'Got file: ' + fn
                #     b_msg = msg.encode(encoding='utf8')
                #     self.sock.sendall(b_msg)
        except OSError:
            received = False
            print("Connection lost ...")
        return received, fn

    def receiveMessage(self):
        data = self.sock.recv(1024)
        print(data)


if __name__ == '__main__':
    client = SocketClient(ip='127.0.0.1')  # local host for debugging, using default IP is ok
    # client.receiveMessage()
    # client.sendFile('clientSaved/UHD.png')
    client.receiveFile('clientSaved')
