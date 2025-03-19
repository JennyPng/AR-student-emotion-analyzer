import socket
import time
import json
import global_vars 

def run_server(host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                # data_list = ["Text 1", "Text 2", "Text 3", "Another Text", "More text"] # Example list
                # json_data = json.dumps(data_list) + "\n" # Add newline for easier parsing on client
                # encoded_data = json_data.encode('utf-8')
                json_data = json.dumps(global_vars.DATA_TO_SEND) + "\n" # Add newline for easier parsing on client
                encoded_data = json_data.encode('utf-8')
                # print(encoded_data)
                try:
                    # print("sending")
                    conn.sendall(encoded_data)
                    time.sleep(0.5) # Send data
                except (ConnectionResetError, BrokenPipeError):
                    print("Client disconnected.")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

if __name__ == "__main__":
    run_server()