import websocket
import asyncio

ws_result_endpoint = "ws://localhost:8000/ws/result"

def main():
    ws = websocket.create_connection(ws_result_endpoint)
    print("Connected to WebSocket server")

    ws.send("FukuroShin")
    print("Test message sent")

    ws.close()
    print("Connection closed")

if __name__ == "__main__":
    main()
