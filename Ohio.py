import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)
        if not client_data:
            break
        
        # Forward data to the remote host
        remote_socket.sendall(client_data)
        
        # Receive data from the remote host
        remote_data = remote_socket.recv(4096)
        if not remote_data:
            break
        
        # Forward data back to the client
        client_socket.sendall(remote_data)
    
    client_socket.close()
    remote_socket.close()

def start_proxy(proxy_host, proxy_port, remote_host, remote_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)
    
    print(f"[*] Proxy listening on {proxy_host}:{proxy_port}")
    
    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        proxy_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()

if __name__ == "__main__":
    proxy_host = "127.0.0.1"  # Proxy listens on localhost
    proxy_port = 8888          # Proxy port
    remote_host = "192.168.1.10"  # Remote host to forward requests
    remote_port = 80           # Remote port
    
    start_proxy(proxy_host, proxy_port, remote_host, remote_port)
