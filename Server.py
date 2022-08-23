import socket
from threading import Thread
import sys, os, uuid, pickle, random
from Objects.Player import Player
from Characters import Characters


PLAYERS_PER_GAME = 10
CONNECTED_PLAYERS = {}

class Server:

    def __init__(self):
        self.server_ip = "192.168.1.38"
        self.port = 4444
        self.server_settings = (self.server_ip, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_index = 0
        self.character = Characters()

    def start(self):
        try:
            self.server_socket.bind(self.server_settings)
        except Exception as e:
            print("[ERROR] Error trying to bind server.", e)

        self.server_socket.listen(PLAYERS_PER_GAME)
        self.listen_connections()
        print(f"[CONNECTION] Listening for connections on {self.port}")

    def listen_connections(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"[CONNECTION] Connection from {addr}")
            ACCEPT_THREAD = Thread(target=self.thread_client, args=(conn, addr, self.player_index))
            ACCEPT_THREAD.start()

    def thread_client(self, conn, addr, player_id):
        player_id = str(uuid.uuid4())
        CONNECTED_PLAYERS[player_id] = ""
        conn.send(str(player_id).encode())
        print("[SERVER] Started thread with player index:", player_id)
        is_online = True
        while is_online:
            try:
                data = conn.recv(2048).decode()
                pid, x, y = self.unpack_received_data(data)
                CONNECTED_PLAYERS[pid] = "{0},{1}".format(x, y)
                ids = list(CONNECTED_PLAYERS.keys())
                list_players = ""
                for id in ids:
                    list_players += "{},{}|".format(id, CONNECTED_PLAYERS[pid])

                if not data:
                    print(f"{addr} has disconnected")
                    is_online = False
                # else:
                #     for player_idx in CONNECTED_PLAYERS:
                #         player = CONNECTED_PLAYERS[player_idx]
                #         if player != current_player:
                #             list_players[player_idx] = player
                
                print("Server Players: ", CONNECTED_PLAYERS)
                conn.sendall(list_players.encode())

            except Exception as e:
                print(f"[SERVER] {addr} has disconnected.", e)
                is_online = False

        print(f"[SERVER] Ended threaded tasks for client: {addr}")
        del CONNECTED_PLAYERS[player_id]
        conn.close()

    def unpack_received_data(self, data):
        unpacked = data.split(",")
        return unpacked

def main():
    server = Server()
    server.start()


if __name__ == '__main__':
    main()