#聊天室 server端
import socket
import select #調用select 使用osi模型 跨平台(windows linux mac)

HEADER_LENGTH = 10#接收長度
IP = "127.0.0.1"
PORT = 1234


#AF: address family
#INET: internet
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#setsocketopt: set socket option
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#1=true

server_socket.bind((IP, PORT))#使用tuple傳入ip and port

server_socket.listen()#監聽

sockets_list = [server_socket]

clients = {}


def recieve_message(client_socket):
    try:
        #rect: recieve
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header): #client斷開連接
            return False

        message_length = int(message_header.decode("utf-8").strip())

        return {"header": message_header, "data": client_socket.recv(message_length)}
        
    except:
        return False


while True:
    #select.select(要讀的socket, 要寫入的socket, 有錯誤發生的socket)
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:#循環讀出
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = recieve_message(client_socket)

            if user is False:#client斷開連接
                 continue

            sockets_list.append(client_socket)

            clients[client_socket] = user#前面已經定義過 內有完整的屬性

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}");

        else:
            message= recieve_message(notified_socket)

            if message is False:
                print(f"Close connection from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket)#移除該socket
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            #訊息發給大家
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
                    
