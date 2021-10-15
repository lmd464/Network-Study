from multiprocessing import Process
import socket
import time

def multiprocess_sr(csocket, addr):

    # 1. Client로부터 데이터를 받음
    data = csocket.recv(1024)
    print(f"[Client {addr} Info] {data.decode()}")

    # 2. HTTP 200 OK, Content-type 전송
    res = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
    csocket.send(res.encode('utf-8'))
    csocket.send(data)

    # 3. close
    csocket.close()


def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen()

    req_clients = list()
    try:
        # 반복 : accept -> recv -> send -> close
        while True:
            # 1. accept : 개별 클라이언트의 정보 받아옴 / csocket : 하나의 클라이언트
            (csocket, addr) = server_socket.accept()

            # 2. client list에 client 넣기
            req_clients.append(csocket)

            # 3. 요청 수 만큼 프로세스 생성(멀티프로세싱), 실행
            for req_client in req_clients:
                proc = Process(target=multiprocess_sr, args=(req_client, addr))
                proc.start()

            # 이미 배정된 클라이언트 리스트 초기화
            req_clients = list()

    except:
        proc.join()


if __name__ == "__main__":
    port = 8890
    main(port)