# # import socket
# # import threading

# # def handle_client(client_socket, client_address, other_client_socket):
# #     while True:
# #         try:
# #             data = client_socket.recv(1024)
# #             if not data:
# #                 print(f"Client {client_address} disconnected")
# #                 break
# #             print(f"Received from {client_address}: {data.decode()}")

# #             other_client_socket.sendall(data)
            
# #         except ConnectionResetError:
# #             print(f"Client {client_address} forcibly disconnected")
# #             break
# #     client_socket.close()

# # def main():
# #     host = '127.0.0.1'
# #     port = 12345

# #     # Create a TCP socket
# #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     server_socket.bind((host, port))
# #     server_socket.listen(5)
# #     print("Server listening...")

# #     try:
# #         client1_socket, client1_address = server_socket.accept()
# #         print(f"Client connected: {client1_address}")

# #         client2_socket, client2_address = server_socket.accept()
# #         print(f"Client connected: {client2_address}")

# #         client1_receive_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket))
# #         client2_receive_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket))

# #         client1_receive_thread.start()
# #         client2_receive_thread.start()

# #         client1_receive_thread.join()
# #         client2_receive_thread.join()

# #     except KeyboardInterrupt:
# #         print("Server shutting down...")
# #         server_socket.close()

# # if __name__ == "__main__":
# #     main()

# import socket
# import threading

# def handle_client(client_socket, client_address, username):
#     while True:
#         try:
#             data = client_socket.recv(1024)
#             if not data:
#                 print(f"Client {client_address} disconnected")
#                 break
            
#             decoded_data = data.decode()
            
#             if decoded_data.startswith("/private"):
#                 # Extract the recipient username and message
#                 recipient_username, message = decoded_data.split(maxsplit=1)[1].split(maxsplit=1)
#                 send_private_message(username, recipient_username, message.encode())
#             else:
#                 print(f"Received from {username}: {decoded_data}")
#                 broadcast_message(username, decoded_data)
            
#         except ConnectionResetError:
#             print(f"Client {client_address} forcibly disconnected")
#             break
#     client_socket.close()

# def broadcast_message(sender_username, message):
#     for client_socket, client_info in clients.items():
#         if client_info["username"] != sender_username:
#             client_socket.sendall(f"Sent by {sender_username} : {message}".encode())

# def send_private_message(sender_username, recipient_username, message):
#     recipient_socket = find_client_socket_by_username(recipient_username)
#     if recipient_socket:
#         recipient_socket.sendall(f"[Private] {sender_username}: {message}".encode())
#     else:
#         sender_socket = find_client_socket_by_username(sender_username)
#         sender_socket.sendall(f"User '{recipient_username}' not found or offline.".encode())

# def find_client_socket_by_username(username):
#     for client_socket, client_info in clients.items():
#         if client_info["username"] == username:
#             return client_socket
#     return None

# def main():
#     host = '127.0.0.1'
#     port = 12345

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(5)
#     print("Server listening...")

#     try:
#         while True:
#             client_socket, client_address = server_socket.accept()
#             print(f"Client connected: {client_address}")

#             username = client_socket.recv(1024).decode()
#             clients[client_socket] = {"address": client_address, "username": username}

#             client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
#             client_thread.start()

#     except KeyboardInterrupt:
#         print("Server shutting down...")
#         server_socket.close()

# if __name__ == "__main__":
#     clients = {}
#     main()

import socket
import threading
import ssl
import hashlib

HashTable = {}

def handle_client(client_socket, client_address, username):
#     client_socket.send(str.encode('ENTER PASSWORD : ')) # Request Password
#     password = client_socket.recv(2048)
#     password = password.decode()
#     username = username.decode()
#     password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
# # REGISTERATION PHASE   
# # If new user,  regiter in Hashtable Dictionary  
#     if username not in HashTable:
#         HashTable[username]=password
#         client_socket.send(str.encode('Registeration Successful')) 
#         print('Registered : ',username)
#         print("{:<8} {:<20}".format('USER','PASSWORD'))
#         for k, v in HashTable.items():
#             label, num = k,v
#             print("{:<8} {:<20}".format(label, num))
#         print("-------------------------------------------")
        
#     else:
# # If already existing user, check if the entered password is correct
#         if(HashTable[username] == password):
#             client_socket.send(str.encode('client_socket Successful')) # Response Code for Connected Client 
#             print('Connected : ',username)
#         else:
#             client_socket.send(str.encode('Login Failed')) # Response code for login failed
#             print('client_socket denied : ',username)
    login_attempts = 3  # Number of allowed login attempts
    while login_attempts > 0:
        client_socket.send(str.encode('ENTER PASSWORD : '))
        password = client_socket.recv(2048).decode()
        password_hash = hashlib.sha256(str.encode(password)).hexdigest()
        if username not in HashTable:
            HashTable[username]=password_hash
            client_socket.send(str.encode('Registeration Successful')) 
            print('Registered : ',username)
            print("{:<8} {:<20}".format('USER','PASSWORD'))
            for k, v in HashTable.items():
                label, num = k,v
                print("{:<8} {:<20}".format(label, num))
            print("-------------------------------------------")
            handle_authenticated_client(client_socket, client_address, username)
            return
        else:
    # If already existing user, check if the entered password is correct
            if(HashTable[username] == password_hash):
                # client_socket.send(str.encode('client_socket Successful')) # Response Code for Connected Client 
                # print('Connected : ',username)
                client_socket.send(str.encode('Login Successful'))
                print(f'Client {username} connected.')
                handle_authenticated_client(client_socket, client_address, username)
                return  # Exit the loop on successful login
            else:
                # client_socket.send(str.encode('Login Failed')) # Response code for login failed
                # print('client_socket denied : ',username)
                login_attempts -= 1
        # Check if username exists and password matches
        # if username in HashTable and HashTable[username] == password_hash:
        #     client_socket.send(str.encode('Login Successful'))
        #     print(f'Client {username} connected.')
        #     handle_authenticated_client(client_socket, client_address, username)
        #     return  # Exit the loop on successful login
        if login_attempts > 0:
            client_socket.sendall(f"Incorrect password. You have {login_attempts} attempts remaining.".encode())
        else:
            client_socket.sendall(b"Login failed. Maximum attempts reached.")
            print(f'Client {username} login failed after {login_attempts + 3} attempts.')
            break  # Exit the loop on failed attempts

    client_socket.close()
def handle_authenticated_client(client_socket, client_address, username):
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
                broadcast_message(username, decoded_data)
            
        except ConnectionResetError:
            print(f"Client {client_address} forcibly disconnected")
            break
    client_socket.close()

def broadcast_message(sender_username, message):
    for client_socket, client_info in clients.items():
        if client_info["username"] != sender_username:
            client_socket.sendall(f"Sent by {sender_username} : {message}".encode())

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

    # Create SSL context and load certificate/key
    context = ssl.create_default_context()
    context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.pem")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening...")

    try:
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='server-cert.pem', keyfile='server-key.pem')
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")

            # Wrap the client socket with SSL context
            client_socket = context.wrap_socket(client_socket, server_side=True)
            client_socket.send(str.encode('ENTER USERNAME : ')) # Request Username
            username = client_socket.recv(2048)
            # username = client_socket.recv(1024).decode()
            clients[client_socket] = {"address": client_address, "username": username}

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    clients = {}
    main()
