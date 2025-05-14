## 여러 메시지 주고 받기
import socket
import threading

# 서버 정보
host = 'localhost'
port = 8888

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## socket.AF_INET : IPv4 주소 체제 사용
    ## socket.AF_INET6 : IPv6 주소 체제 사용
    ## socket.SOCK_STREAM : TCP 통신 사용
    ## socket.SOCK_DGRAM : UDP 통신 사용

# 서버에 연결
client_socket.connect((host, port))
print('서버 연결됨')

def recvThread():
    while True:
        # 클라이언트로부터 데이터 수신
        data = client_socket.recv(1024)
        print('수신한 데이터:', data.decode('utf-8'))

t1 = threading.Thread(target = recvThread, args=())
t1.start()

while True:
    # 클라이언트로 데이터 전송
    message = input()
    client_socket.send(message.encode('utf-8'))

# 소켓 닫기
client_socket.close()
