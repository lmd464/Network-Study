import socket
from random import randint

TCP_IP = '192.168.0.24'
TCP_PORT = 5001

# socket -> bind -> listen -> accept
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))

# Socket 으로 오는 connect 요청 listen, 3개까지 accept
# accept 과정에서 conn 이 나오는데, 이를 이용하면 한 소켓에 여러 연결 가능
# 한 개의 conn 은 각 인스턴스의 연결
connections = []
while True:
    sock.listen()
    conn, addr = sock.accept()
    connections.append(conn)
    print('Connection address : ' + str(addr))
    if len(connections) == 3:
        break

# 개별 connection 들에 메시지 보냄
for conn in connections:
    conn.send("Okay... All players have gathered. Start the game.\n" \
              "Please select 1 number from 1 to 10.".encode())


# Client 가 선택할 난수생성
ten_random_numbers = []
for i in range(10):
    ten_random_numbers.append(randint(1, 101))

# Client 별로 할당할 난수 생성
four_random_numbers = []
for i in range(4):
    four_random_numbers.append(randint(-1, 5))


# accept 완료
# send/recv 수행 후 -> close

# 3개의 클라이언트로부터 숫자 입력 받아옴
choose_result_list = []
for conn in connections:

    # input number 받음
    data = conn.recv(1024)
    if not data: break
    received_number = data.decode()

    # SERVER LOG
    print('Received Data : ' + received_number)

    # input number 결과 보냄
    choose_result = ten_random_numbers[int(received_number)]
    choose_result_list.append(choose_result)
    choose_result_prompt = "You chose the number " + str(choose_result) + ". Please wait."
    conn.send(choose_result_prompt.encode())



# 3개의 클라이언트로부터 arith 입력 받아옴, 계산
final_result_list = []
conn_idx = 0
for conn in connections:

    # arith 선택 안내 전송
    temp = "Do you want multiply or add...?"
    conn.send(temp.encode())

    # input arith 받음
    data = conn.recv(1024)
    if not data: break
    received_arith = data.decode()

    # SERVER LOG
    print('Received arith : ' + received_arith)

    # 고른 순번의 난수와, 사용자 별 할당된 난수를 계산하여 보내기
    final_result = -10000
    if received_arith == "add":
        final_result = choose_result_list[conn_idx] + four_random_numbers[conn_idx]

    elif received_arith == "multiply":
        final_result = choose_result_list[conn_idx] * four_random_numbers[conn_idx]

    else:
        for conn in connections:
            conn.close()
        print("error. plz retry")

    final_result_list.append(final_result)

    # SERVER LOG
    print('Received result : ' + str(final_result))

    conn.send("Okay... please wait.".encode())

    conn_idx += 1


# 승자 확인
win_number = max(final_result_list)
for conn_idx in range(len(connections)):
    if final_result_list[conn_idx] == win_number:
        connections[conn_idx].send("Congratulations. You won!".encode())
    else:
        connections[conn_idx].send("Unfortunately, you have been defeated.".encode())


# Connection 들 전부 닫기
for conn in connections:
    conn.close()
