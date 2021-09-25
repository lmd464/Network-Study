import socket

TCP_IP = '192.168.0.24'
TCP_PORT = 5001

# socket -> connect -> send / recv -> close
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))


# 3명 다 모였을때의 확인 & 숫자입력 메시지 기다림
print(sock.recv(1024).decode())

# 숫자 입력 보냄
sock.send(input("Number : ").encode())

# 숫자 결과 받음
print(sock.recv(1024).decode())


# 3명에게 숫자 입력 다 받았을 때의 확인 메시지 기다림
print(sock.recv(1024).decode())

# 연산 입력 보냄
sock.send(input("multiply or add : ").encode())

# 결과 기다리라는 알림 받음
print(sock.recv(1024).decode())

# 최종 결과 받음
print(sock.recv(1024).decode())

sock.close()
