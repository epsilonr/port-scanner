from concurrent.futures import ThreadPoolExecutor
from utils import get_service_name
import socket
import argparse

TARGET_IP = ""

PORT_START = -1
PORT_END = -1

TIMEOUT = 3

WORKER_COUNT = 200

open_ports = []


def check_socket(ip: str, port: int):
    try:
        with socket.create_connection((ip, port), timeout=TIMEOUT) as s:
            open_ports.append(port)
            s.send(b'GET / HTTP/1.1\r\n\r\n')
            banner = s.recv(1024)
            print("Banner: " + banner.decode("utf-8").strip())
    except Exception as e:
        print(e)
        pass
    
def is_valid_ip():
    global TARGET_IP

    if not TARGET_IP:
        return False

    if (len(TARGET_IP.split(".")) != 4):
        TARGET_IP = socket.gethostbyname(TARGET_IP)

    try:
        socket.inet_aton(TARGET_IP)
        return True
    except socket.error:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple port scanner written in python.")

    parser.add_argument("ip", help="IP of the target server.")
    parser.add_argument("-p", nargs=2, help="Beginning / ending port pair to scan.")
    parser.add_argument("-t", type=float, help="Timeout for each port scan.")
    parser.add_argument("-w", type=int, help="Maximum worker thread count that runs simultaneously.")

    args = parser.parse_args()

    TARGET_IP = args.ip

    PORT_START = -1
    PORT_END = -1

    if args.t is not None:
        TIMEOUT = args.t

    if args.w is not None:
        WORKER_COUNT = args.w

    if args.p is not None:
        if args.p[0] == "-":
            args.p[0] = "0"
        
        if args.p[1] == "-":
            args.p[1] = "65535"

        if not args.p[0].isdigit() or not args.p[1].isdigit():
            print("Invalid port distance pair.")
            exit()
        else:
            PORT_START = int(args.p[0])
            PORT_END = int(args.p[1])
    else:
        PORT_START = 0
        PORT_END = 65535

    if not is_valid_ip():
        print(f"Invalid IP: {TARGET_IP}")
        exit()

    print(f"\nScanning {TARGET_IP} from port {PORT_START} to {PORT_END}...\n")

    pool = ThreadPoolExecutor(max_workers=WORKER_COUNT)

    for port in range(PORT_START, PORT_END + 1):
        pool.submit(check_socket, TARGET_IP, port)

    pool.shutdown(wait=True)

    for port in open_ports:
        print(f"Port {port} is open. Service: {get_service_name(port)}")

    # for result in sorted(results.items(), key=lambda item: item[0]):
    #     print(result)