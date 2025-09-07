from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from websocket_client import VoxtaClient
from panda3d.core import DirectionalLight, AmbientLight, VBase4
import sys
import time

class Game(ShowBase):
    def __init__(self):
        super().__init__(windowType='offscreen')
        print("Game: Initializing with advanced graphics...")

        # --- Graphics Polish ---
        # Enable the shader generator for advanced effects like PBR and shadows
        self.render.setShaderAuto()

        # Add a nice skybox for the background
        self.skybox = self.loader.loadModel("models/environment")
        self.skybox.reparentTo(self.render)
        self.skybox.setScale(100) # Make it large enough to encompass the scene
        self.skybox.setZ(-10)

        # Add an ambient light for general illumination
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # Add a strong directional light to cast shadows
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.8, 0.7, 0.6, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        # Enable shadows for the directional light
        dlight.setShadowCaster(True, 1024, 1024)
        self.render.setShaderInput("light", dlnp) # Pass the light to the shader

        # --- Character Setup ---
        try:
            self.character = Actor("../assets/RiggedSimple.glb")
            self.character.reparentTo(self.render)
            # The model is small, scale it up
            self.character.setScale(2.0)
            self.character.setHpr(180, 0, 0) # Turn it to face the camera

            self.valid_anims = self.character.getAnimNames()
            print(f"Game: Character loaded with animations: {self.valid_anims}")
        except Exception as e:
            print(f"Game: CRITICAL - Failed to load character model: {e}", file=sys.stderr)
            sys.exit(1)

        # --- WebSocket Client ---
        print("Game: Starting WebSocket client...")
        self.ws_client = VoxtaClient()
        self.ws_client.start()

        # Add a task to check for new animations
        self.taskMgr.add(self.check_animation_queue, "checkAnimationQueueTask")
        print("Game: Added animation check task.")

    def check_animation_queue(self, task):
        anim_name = self.ws_client.get_next_animation()
        if anim_name:
            print(f"Game Task: Received animation command: '{anim_name}'")
            if anim_name in self.valid_anims:
                if self.character.getCurrentAnim() != anim_name:
                    print(f"Game Task: Playing new animation: '{anim_name}'")
                    self.character.loop(anim_name) # Loop is better for continuous states
            else:
                print(f"Game Task: WARNING - Received unknown animation name: '{anim_name}'")
        return task.cont

# --- Main execution block for testing ---
if __name__ == '__main__':
    print("Main: Setting up game application...")
    try:
        app = Game()
        print("Main: Application setup complete.")

        # Simulate runtime by stepping the task manager
        print("Main: Simulating 5 seconds of runtime...")
        end_time = time.time() + 5
        while time.time() < end_time:
            app.taskMgr.step()
            time.sleep(0.1)

        print("Main: Simulation finished.")

    except Exception as e:
        print(f"Main: An error occurred during app setup or run: {e}", file=sys.stderr)
    finally:
        if 'app' in locals() and hasattr(app, 'ws_client'):
            print("Main: Stopping WebSocket client...")
            app.ws_client.stop()
        print("Main: Script finished.")
