import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    while True:
        response = client.recv(4096).decode('utf-8')
        if not response:
            break
        print(response, end='')

        if "Goodbye!" in response:
            break

        if "Enter amount" in response:
            amount = input()
            client.sendall(amount.encode('utf-8'))
        else:
            option = input()
            client.sendall(option.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()