# import socket
# import threading

# def handle_client(client_socket, client_address, other_client_socket):
#     while True:
#         try:
#             data = client_socket.recv(1024)
#             if not data:
#                 print(f"Client {client_address} disconnected")
#                 break
#             print(f"Received from {client_address}: {data.decode()}")

#             other_client_socket.sendall(data)
            
#         except ConnectionResetError:
#             print(f"Client {client_address} forcibly disconnected")
#             break
#     client_socket.close()

# def main():
#     host = '127.0.0.1'
#     port = 12345

#     # Create a TCP socket
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(5)
#     print("Server listening...")

#     try:
#         client1_socket, client1_address = server_socket.accept()
#         print(f"Client connected: {client1_address}")

#         client2_socket, client2_address = server_socket.accept()
#         print(f"Client connected: {client2_address}")

#         client1_receive_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket))
#         client2_receive_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket))

#         client1_receive_thread.start()
#         client2_receive_thread.start()

#         client1_receive_thread.join()
#         client2_receive_thread.join()

#     except KeyboardInterrupt:
#         print("Server shutting down...")
#         server_socket.close()

# if __name__ == "__main__":
#     main()

import socket
import threading

def handle_client(client_socket, client_address, username):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected")
                break
            
            decoded_data = data.decode()
            
            if decoded_data.startswith("/private"):
                # Extract the recipient username and message
                recipient_username, message = decoded_data.split(maxsplit=1)[1].split(maxsplit=1)
                send_private_message(username, recipient_username, message.encode())
            else:
                print(f"Received from {username}: {decoded_data}")
                broadcast_message(username, decoded_data.encode())
            
        except ConnectionResetError:
            print(f"Client {client_address} forcibly disconnected")
            break
    client_socket.close()

def broadcast_message(sender_username, message):
    for client_socket, client_info in clients.items():
        if client_info["username"] != sender_username:
            client_socket.sendall(message)

def send_private_message(sender_username, recipient_username, message):
    recipient_socket = find_client_socket_by_username(recipient_username)
    if recipient_socket:
        recipient_socket.sendall(f"[Private] {sender_username}: {message}".encode())
    else:
        sender_socket = find_client_socket_by_username(sender_username)
        sender_socket.sendall(f"User '{recipient_username}' not found or offline.".encode())

def find_client_socket_by_username(username):
    for client_socket, client_info in clients.items():
        if client_info["username"] == username:
            return client_socket
    return None

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")

            username = client_socket.recv(1024).decode()
            clients[client_socket] = {"address": client_address, "username": username}

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    clients = {}
    main()
