import socket
import threading

# Define the bank accounts
accounts = {
    'user1': {'password': 'pass1', 'balance': 1000},
    'user2': {'password': 'pass2', 'balance': 1500}
}

# Lock for thread safety
lock = threading.Lock()


def handle_client(client_socket):
    try:
        client_socket.sendall(b"Welcome to the Bank ATM. Please log in.\nUsername: ")
        username = client_socket.recv(1024).decode('utf-8').strip()
        client_socket.sendall(b"Password: ")
        password = client_socket.recv(1024).decode('utf-8').strip()

        if username in accounts and accounts[username]['password'] == password:
            client_socket.sendall(
                b"Login successful.\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n")
            while True:
                option = client_socket.recv(1024).decode('utf-8').strip()

                if option == '1':
                    balance = accounts[username]['balance']
                    client_socket.sendall(
                        f"Your balance is: ${balance}\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n".encode(
                            'utf-8'))

                elif option == '2':
                    client_socket.sendall(b"Enter amount to deposit: ")
                    amount = client_socket.recv(1024).decode('utf-8').strip()
                    print(f"Received deposit amount: {amount}")  # Debugging output
                    try:
                        amount = int(amount)
                        with lock:
                            accounts[username]['balance'] += amount
                        client_socket.sendall(
                            f"${amount} deposited. New balance: ${accounts[username]['balance']}\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n".encode(
                                'utf-8'))
                    except ValueError:
                        client_socket.sendall(
                            b"Invalid amount. Try again.\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n")

                elif option == '3':
                    client_socket.sendall(b"Enter amount to withdraw: ")
                    amount = client_socket.recv(1024).decode('utf-8').strip()
                    print(f"Received withdraw amount: {amount}")  # Debugging output
                    try:
                        amount = int(amount)
                        with lock:
                            if amount <= accounts[username]['balance']:
                                accounts[username]['balance'] -= amount
                                client_socket.sendall(
                                    f"${amount} withdrawn. New balance: ${accounts[username]['balance']}\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n".encode(
                                        'utf-8'))
                            else:
                                client_socket.sendall(
                                    b"Insufficient funds.\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n")
                    except ValueError:
                        client_socket.sendall(
                            b"Invalid amount. Try again.\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n")

                elif option == '4':
                    client_socket.sendall(
                        f"Your final balance is: ${accounts[username]['balance']}\nGoodbye!\n".encode('utf-8'))
                    break

                else:
                    client_socket.sendall(
                        b"Invalid option. Try again.\nChoose an option: [1] Check Balance, [2] Deposit, [3] Withdraw, [4] Exit\n")
        else:
            client_socket.sendall(b"Login failed. Goodbye!\n")
    finally:
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()

