import socket
import cv2
import numpy as np
import threading

def receive_video(client_socket):
    cv2.namedWindow("Received Video - Client 2", cv2.WINDOW_NORMAL)
    
    while True:
        try:
            data = client_socket.recv(4096*256)
            if not data:
                print("Disconnected from server.")
                break
            
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            print(frame)
            if frame is None:
                print("Error: Failed to decode frame")
                continue
            
            cv2.imshow("Received Video - Client 2", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        except Exception as e:
            print("Error receiving frame:", e)
            break

    cv2.destroyAllWindows()
    
def send_video(client_socket):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, img_encoded = cv2.imencode('.jpg', frame, encode_param)
        
        try:
            client_socket.sendall(img_encoded.tobytes())
        except ConnectionResetError:
            print("Server disconnected.")
            break
        cv2.waitKey(10)

    cap.release()
    cv2.destroyAllWindows()

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print("Connected to server.")

        send_thread = threading.Thread(target=send_video, args=(client_socket,))
        receive_thread = threading.Thread(target=receive_video, args=(client_socket,))
        
        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()

    except ConnectionRefusedError:
        print("Server is not available.")
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
