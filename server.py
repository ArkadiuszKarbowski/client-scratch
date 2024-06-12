import socket
import threading
import time

DEST_IP = '127.0.0.1'  
DEST_PORT = 42001 
SERV_IP = 0       
SERV_PORT = 42002

values = {}

def calculate_mean_and_send(values:dict, udp_to_scratch_socket:socket.socket):
    mean_value = int(sum(values.values()) / len(values))
    print(f"Current mean value of received integers: {mean_value}")
    data = f'sensor-update \"left_y\" {mean_value}\n'
    udp_to_scratch_socket.sendto(data.encode(), (DEST_IP, DEST_PORT))

def start_server(host=SERV_IP, port=SERV_PORT):
    udp_to_scratch_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f'Server listening on {host}:{port}')
        
        while True:
            data, addr = s.recvfrom(1024)  # buffer size is 1024 bytes
            print(f"received message: {data} from: {addr}")         
            player_num, value = data.split()
            values[player_num] = int(value)

            calculate_mean_and_send(values, udp_to_scratch_socket)


if __name__ == "__main__":
    start_server()