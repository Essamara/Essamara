from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from websocket_client import VoxtaClient
from panda3d.core import DirectionalLight, AmbientLight, VBase4
import sys
import time
import argparse

class Game(ShowBase):
    def __init__(self, args):
        # Determine window type based on the --headless flag
        window_type = 'offscreen' if args.headless else 'onscreen'
        super().__init__(windowType=window_type)

        print("Game: Initializing...")

        # --- Graphics Polish ---
        self.render.setShaderAuto()
        self.skybox = self.loader.loadModel("models/environment")
        self.skybox.reparentTo(self.render)
        self.skybox.setScale(100)
        self.skybox.setZ(-10)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.8, 0.7, 0.6, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)
        dlight.setShadowCaster(True, 1024, 1024)
        self.render.setShaderInput("light", dlnp)

        # --- Character Setup ---
        try:
            self.character = Actor("../assets/RiggedSimple.glb")
            self.character.reparentTo(self.render)
            self.character.setScale(2.0)
            self.character.setHpr(180, 0, 0)
            self.valid_anims = self.character.getAnimNames()
            print(f"Game: Character loaded with animations: {self.valid_anims}")
        except Exception as e:
            print(f"Game: CRITICAL - Failed to load character model: {e}", file=sys.stderr)
            sys.exit(1)

        # --- Conditionally start the WebSocket Client ---
        self.ws_client = None
        if not args.no_ws:
            print("Game: Starting WebSocket client...")
            self.ws_client = VoxtaClient()
            self.ws_client.start()
            self.taskMgr.add(self.check_animation_queue, "checkAnimationQueueTask")
            print("Game: Added animation check task.")
        else:
            print("Game: WebSocket client is disabled by --no-ws flag.")

    def check_animation_queue(self, task):
        if self.ws_client:
            anim_name = self.ws_client.get_next_animation()
            if anim_name:
                print(f"Game Task: Received animation command: '{anim_name}'")
                if anim_name in self.valid_anims:
                    if self.character.getCurrentAnim() != anim_name:
                        print(f"Game Task: Playing new animation: '{anim_name}'")
                        self.character.loop(anim_name)
                else:
                    print(f"Game Task: WARNING - Received unknown animation name: '{anim_name}'")
        return task.cont

# --- Main execution block ---
if __name__ == '__main__':
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Panda3D Voxta Character Engine")
    parser.add_argument('--no-ws', action='store_true', help="Disable the WebSocket client.")
    parser.add_argument('--headless', action='store_true', help="Run in headless (offscreen) mode.")
    args = parser.parse_args()

    print("Main: Setting up game application...")
    app = None
    try:
        app = Game(args)
        print("Main: Application setup complete.")

        if args.headless:
            print("Main: Headless mode detected. Simulating 5 seconds of runtime...")
            end_time = time.time() + 5
            while time.time() < end_time:
                app.taskMgr.step()
                time.sleep(0.1)
            print("Main: Simulation finished.")
        else:
            print("Main: Starting interactive application loop.")
            app.run() # This starts the main, blocking loop for the interactive window

    except Exception as e:
        print(f"Main: An error occurred during app setup or run: {e}", file=sys.stderr)
    finally:
        if app and app.ws_client:
            print("Main: Stopping WebSocket client...")
            app.ws_client.stop()
        print("Main: Script finished.")
