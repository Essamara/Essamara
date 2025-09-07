import asyncio
import websockets
import json

# Define the handler at the top level
async def server_handler(websocket, path):
    """
    A simple handler that sends one message and then allows the server to close.
    """
    print("Mock Server: Client connected.")
    message = {
        "type": "appTrigger",
        "action": "SwitchState",
        "stateName": "Cylinder"
    }
    await websocket.send(json.dumps(message))
    print(f"Mock Server: Sent message: {json.dumps(message)}")
    # The client will close the connection, which will allow the server to exit.

async def main():
    """
    A short-lived mock server that runs until one client has been served.
    """
    # The server will automatically exit once the handler is done
    # and the client has disconnected.
    async with websockets.serve(server_handler, "localhost", 8765):
        # We need to keep the main coroutine alive until the server's task is done.
        # Since the server runs in the background, we'll just wait for it to close.
        # This is a bit tricky, so we'll just use a timeout.
        try:
            # Wait for a future that will never be set, with a timeout.
            await asyncio.wait_for(asyncio.Future(), timeout=5.0)
        except asyncio.TimeoutError:
            pass

if __name__ == "__main__":
    print("Mock Server: Starting...")
    try:
        asyncio.run(main())
        print("Mock Server: Shutdown complete.")
    except Exception as e:
        print(f"Mock Server: An error occurred: {e}")
