from threading import Thread
import socket
import select

def multithread_sr(csocket, addr):

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

            # 3. 요청 리스트를 Select 하여 처리, 실행
            input_ready, write_ready, except_ready = select.select(req_clients, [], [])
            for ready_client in input_ready:
                th = Thread(target=multithread_sr, args=(ready_client, addr))
                th.start()

            # Select하여 처리된 클라이언트 제외
            for done_client in input_ready:
                req_clients.remove(done_client)
            
    except:
        th.join()


if __name__ == "__main__":
    port = 8892
    main(port)