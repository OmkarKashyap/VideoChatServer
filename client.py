import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            print(f"Received from server: {data.decode()}")
        except ConnectionResetError:
            print("Disconnected from server.")
            break

def send_messages(client_socket):
    while True:
        # Send message to the server
        message = input("Enter message to send: ")
        client_socket.sendall(message.encode())

def main():
    # Server configuration
    host = '127.0.0.1'
    port = 12345

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print("Connected to server.")

        # Create threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        # Start threads
        receive_thread.start()
        send_thread.start()

        # Join threads
        receive_thread.join()
        send_thread.join()

    except ConnectionRefusedError:
        print("Server is not available.")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
