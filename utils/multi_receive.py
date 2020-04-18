from utils import SocketClient


def multi_receive(client, save_path):
    received, fn = client.receiveFile()
    if received and fn.split('.')[-1] == 'txt':
        num = int(fn.split('.')[0])
        for i in range(num):
            received, fn = client.receiveFile(save_path)
            if not received:
                print(fn + 'failed to receive.')
    return received


if __name__ == '__main__':
    client = SocketClient(ip='127.0.0.1')
    save_path = 'saved'
    multi_receive(client, save_path)
