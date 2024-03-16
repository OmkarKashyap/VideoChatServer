# # # import socket
# # # import threading

# # # def receive_messages(client_socket):
# # #     while True:
# # #         try:
# # #             # Receive data from the server
# # #             data = client_socket.recv(1024)
# # #             if not data:
# # #                 print("Disconnected from server.")
# # #                 break
# # #             print(f"Received from server: {data.decode()}")
# # #         except ConnectionResetError:
# # #             print("Disconnected from server.")
# # #             break

# # # def send_messages(client_socket):
# # #     while True:
# # #         # Send message to the server
# # #         message = input("Enter message to send: ")
# # #         client_socket.sendall(message.encode())

# # # def main():
# # #     # Server configuration
# # #     host = '127.0.0.1'
# # #     port = 12345

# # #     # Create a TCP socket
# # #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # #     try:
# # #         # Connect to the server
# # #         client_socket.connect((host, port))
# # #         print("Connected to server.")

# # #         # Create threads for sending and receiving messages
# # #         receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
# # #         send_thread = threading.Thread(target=send_messages, args=(client_socket,))

# # #         # Start threads
# # #         receive_thread.start()
# # #         send_thread.start()

# # #         # Join threads
# # #         receive_thread.join()
# # #         send_thread.join()

# # #     except ConnectionRefusedError:
# # #         print("Server is not available.")

# # #     finally:
# # #         client_socket.close()

# # # if __name__ == "__main__":
# # #     main()

# # import socket
# # import threading

# # def receive_messages(client_socket):
# #     while True:
# #         try:
# #             data = client_socket.recv(1024)
# #             if not data:
# #                 print("Disconnected from server.")
# #                 break
# #             print(f"{data.decode()}")
# #         except ConnectionResetError:
# #             print("Disconnected from server.")
# #             break

# # def send_messages(client_socket):
# #     while True:
# #         message = input("Enter message to send: ")
# #         client_socket.sendall(message.encode())

# # def main():
# #     host = '127.0.0.1'
# #     port = 12345

# #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# #     try:
# #         client_socket.connect((host, port))
# #         print("Connected to server.")

# #         username = input("Enter your username: ")
# #         client_socket.sendall(username.encode())

# #         receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
# #         send_thread = threading.Thread(target=send_messages, args=(client_socket,))

# #         receive_thread.start()
# #         send_thread.start()

# #         receive_thread.join()
# #         send_thread.join()

# #     except ConnectionRefusedError:
# #         print("Server is not available.")

# #     finally:
# #         client_socket.close()

# # if __name__ == "__main__":
# #     main()

import socket
import threading
import ssl

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            print(f"{data.decode()}")
        except ConnectionResetError:
            print("Disconnected from server.")
            break
        except OSError as e:
            if e.errno == 9:  # Bad file descriptor error
                print("Socket closed.")
                client_socket.close()
                break
            else:
                raise  # Re-raise other OSError exceptio

def send_messages(client_socket):
    while True:
        message = input("Enter message to send: ")
        client_socket.sendall(message.encode())

def main():
    host = '127.0.0.1'
    port = 12345

    # Create SSL context (disable hostname verification for self-signed cert)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server-cert.pem')
    context.check_hostname = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    success = True
    try:
        # Wrap the socket with SSL
        client_socket = context.wrap_socket(client_socket)

        client_socket.connect((host, port))
        print("Connected to server.")

        # username = input("Enter your username: ")
        # client_socket.sendall(username.encode())
        response = client_socket.recv(2048)
        # Input UserName
        name = input(response.decode())	
        client_socket.send(str.encode(name))
        while True:

            response = client_socket.recv(2048)
            # Input Password
            password = input(response.decode())	
            client_socket.send(str.encode(password))
            ''' Response : Status of Connection :
                1 : Registeration successful 
                2 : Connection Successful
                3 : Login Failed
            '''
            # Receive response 
            response = client_socket.recv(2048)
            response = response.decode()
            print(response)
            if response.startswith("Login failed"):
                success = False
                break
            elif response.startswith("Login Successful") or response.startswith("Registeration Successful"):
                break
       
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        if success:
            receive_thread.start()
            send_thread.start()

            receive_thread.join()
            send_thread.join()
        else:
            client_socket.close()

    except ConnectionRefusedError:
        print("Server is not available.")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
