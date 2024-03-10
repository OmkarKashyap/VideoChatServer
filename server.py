import socket
import threading

def handle_client(client_socket, client_address, other_client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected")
                break
            print(f"Received from {client_address}: {data.decode()}")

            other_client_socket.sendall(data)
            
        except ConnectionResetError:
            print(f"Client {client_address} forcibly disconnected")
            break
    client_socket.close()

def main():
    host = '127.0.0.1'
    port = 12345

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening...")

    try:
        client1_socket, client1_address = server_socket.accept()
        print(f"Client connected: {client1_address}")

        client2_socket, client2_address = server_socket.accept()
        print(f"Client connected: {client2_address}")

        client1_receive_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket))
        client2_receive_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket))

        client1_receive_thread.start()
        client2_receive_thread.start()

        client1_receive_thread.join()
        client2_receive_thread.join()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    main()
