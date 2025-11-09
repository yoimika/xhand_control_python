import socket

def start_server(host='0.0.0.0', port=54321):  # 改为0.0.0.0监听所有接口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"服务器已启动，监听 {host}:{port} (外部可访问)")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"接收到来自 {addr} 的连接")
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    print(f"接收到数据: {data.decode('ASCII')}")
                    conn.sendall(b"Message received")

