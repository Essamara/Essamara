import asyncio
import websockets
import json
import threading
from collections import deque
import time

class VoxtaClient:
    """
    A WebSocket client that connects to a Voxta-like server, listens for
    animation commands, and makes them available to the main application
    thread via a queue.
    """
    def __init__(self, uri="ws://localhost:8765"):
        self.uri = uri
        self.animation_queue = deque()
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run_client_loop, daemon=True)
        self.is_connected = False

    async def _client_handler(self):
        """
        The core async task that connects and listens for messages.
        """
        while not self._stop_event.is_set():
            try:
                async with websockets.connect(self.uri) as websocket:
                    print("WebSocket client connected to server.")
                    self.is_connected = True
                    while not self._stop_event.is_set():
                        message_str = await websocket.recv()
                        print(f"Client received: {message_str}")
                        try:
                            message = json.loads(message_str)
                            if message.get("type") == "appTrigger" and "stateName" in message:
                                state_name = message["stateName"]
                                print(f"Queueing animation: {state_name}")
                                self.animation_queue.append(state_name)
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON from server: {message_str}")
            except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError) as e:
                self.is_connected = False
                print(f"Connection lost or refused: {e}. Retrying in 3 seconds...")
                await asyncio.sleep(3)
            except Exception as e:
                self.is_connected = False
                print(f"An unexpected error occurred in WebSocket client: {e}")
                await asyncio.sleep(3)

    def _run_client_loop(self):
        """
        Runs the asyncio event loop for the client.
        """
        asyncio.run(self._client_handler())

    def start(self):
        """
        Starts the WebSocket client in a background thread.
        """
        if not self.thread.is_alive():
            self.thread.start()
            print("WebSocket client thread started.")

    def stop(self):
        """
        Signals the client thread to stop.
        """
        self._stop_event.set()
        # The thread will exit on its own.
        print("WebSocket client stop signal sent.")

    def get_next_animation(self):
        """
        Pops the next animation command from the queue. Thread-safe.
        """
        if self.animation_queue:
            return self.animation_queue.popleft()
        return None

if __name__ == '__main__':
    # This block allows for standalone testing of the client.
    print("Running WebSocket client in standalone test mode.")

    async def run_test():
        print("Client Test: Attempting to connect to ws://localhost:8765")
        uri = "ws://localhost:8765"
        try:
            async with websockets.connect(uri) as websocket:
                print("Client Test: Connected successfully.")
                message_str = await websocket.recv()
                print(f"Client Test: Received message: {message_str}")

                # Verify the message
                message = json.loads(message_str)
                if message.get("stateName") == "Cylinder":
                    print("Client Test: SUCCESS - stateName is correct.")
                else:
                    print(f"Client Test: FAILURE - Unexpected stateName: {message.get('stateName')}")
        except Exception as e:
            print(f"Client Test: An error occurred: {e}")

    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        print("Client test stopped.")
