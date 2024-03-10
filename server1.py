import socket
import os
import pickle

def main():
    server_ip = "127.0.0.1"  # Change this to the IP address of your server
    server_port = 8081  # Change this to the port you want the server to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Server listening on ({server_ip}, {server_port})")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Get the hostname of the client
        hostname = socket.gethostbyaddr(client_address[0])[0]
        client_socket.send(hostname.encode())

        # Simulate a list of shared files for each file type (e.g., Videos and Docs)
        shared_files = [["video1.mp4", "video2.mp4"], ["doc1.pdf", "doc2.docx"]]
        shared_files_data = pickle.dumps(shared_files)
        client_socket.send(shared_files_data)

        # Handle file download request
        file_request = client_socket.recv(1024).decode()
        send_file(client_socket, file_request)

        client_socket.close()
        print(f"Connection with {client_address} closed")

def send_file(client_socket, filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            client_socket.send(b"File Exists")
            client_socket.send(str(len(file_data)).encode())
            client_socket.send(file_data)
    except FileNotFoundError:
        client_socket.send(b"File Not Found")

if __name__ == '__main__':
    main()
