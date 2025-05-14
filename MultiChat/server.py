import socket
import threading

# 클라이언트 소켓 정보를 저장할 리스트
client_sockets = []

# 클라이언트와 통신하는 함수
def handle_client(client_socket, address):
    print(f'[{address[0]}:{address[1]}] 클라이언트가 연결되었습니다.')
    while True:
        # 클라이언트로부터 데이터를 받음
        data = client_socket.recv(1024)
        if not data:
            # 클라이언트가 연결을 끊었을 때, 소켓 정보를 리스트에서 제거
            client_sockets.remove(client_socket)
            print(f"{client_socket} disconnected")
            break
        print(f'[{address[0]}:{address[1]}] 수신한 데이터:', data.decode('utf-8'))

        # 다른 클라이언트에게 데이터를 전송
        for socket in client_sockets:
            if socket != client_socket:
                socket.sendall(data)

# 서버의 IP 주소와 포트 번호
host = 'localhost'
port = 8888

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 소켓 바인딩
server_socket.bind((host, port))
server_socket.listen()

print("Server started")

# 클라이언트 접속 대기
while True:
    client_socket, addr = server_socket.accept()
    
    # 새로운 클라이언트 소켓 정보를 리스트에 추가
    client_sockets.append(client_socket)
    
    # 클라이언트와 통신하는 쓰레드 시작
    t = threading.Thread(target=handle_client, args=(client_socket, addr))
    t.daemon = True
    t.start()
