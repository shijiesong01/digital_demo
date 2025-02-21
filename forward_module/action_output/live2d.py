import socket
import subprocess
import time


def live2d_unity_init():
    server_socket = None
    connection = None
    try:
        # 启动 Unity 服务（假设 Unity 项目打包成可执行文件）
        unity_executable_path = "E:\code\\unity\\live-exe\live.exe"
        subprocess.Popen(unity_executable_path)

        # 创建一个 TCP/IP 套接字
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定地址和端口
        server_address = ('localhost', 8888)
        server_socket.bind(server_address)

        # 监听连接
        server_socket.listen(1)

        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        print(f'Connection from {client_address}')

        # 发送初始消息给 Unity
        initial_message = "Initial message from Python"
        connection.sendall(initial_message.encode())

        # 等待 Unity 的响应（可选）
        data = connection.recv(1024)
        print(f'Received from Unity: {data.decode()}')

        return connection

    except Exception as e:
        print(f"Error during connection: {e}")
        if connection:
            connection.close()
    finally:
        if server_socket:
            server_socket.close()
    return None



def live2d_unity_update(connection, move):
    if connection and connection.fileno() != -1:  # 检查套接字是否有效
        try:
            # 发送动作参数给 Unity
            move_message = str(move)
            connection.sendall(move_message.encode())

            # 等待 Unity 的响应（可选）
            data = connection.recv(1024)
            print(f'Received from Unity after sending move: {data.decode()}')
        except Exception as e:
            print(f"Error sending move data: {e}")
            connection.close()
    else:
        print("Invalid socket connection.")



# # 触发 live2unity 函数
# connection = live2d_unity_init()

# if connection:
#     print('goooooood')
#     time.sleep(10)
#     # 触发更新函数，发送动作参数 'Q'
#     live2d_unity_update(connection, 'proud')
#     # 触发更新函数，发送动作参数 'W'
#     #update_move(connection, 'thinking')