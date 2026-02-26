import json
import time
import threading
from pynput import mouse, keyboard

class AutoClicker:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.running = False
        self.program_running = True
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            print(f"Configuration loaded. Hotkey: {self.config.get('hotkey', '<f8>')}")
            if 'description' in self.config:
                print(f"Description: {self.config['description']}")
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {"hotkey": "<f8>", "actions": []}

    def execute_action(self, action):
        if not self.running:
            return

        action_type = action.get('type')
        
        if action_type == 'click':
            button_str = action.get('button', 'left')
            button = mouse.Button.left if button_str == 'left' else mouse.Button.right
            hold_time = action.get('hold_time', 0.1)
            
            print(f"Clicking {button_str} button (hold: {hold_time}s)")
            self.mouse_controller.press(button)
            time.sleep(hold_time)
            self.mouse_controller.release(button)
            
        elif action_type == 'key_press':
            key_str = action.get('key')
            hold_time = action.get('hold_time', 0.1)
            
            if key_str:
                print(f"Pressing key: {key_str} (hold: {hold_time}s)")
                
                # Handle special keys
                key = key_str
                if hasattr(keyboard.Key, key_str):
                    key = getattr(keyboard.Key, key_str)
                
                self.keyboard_controller.press(key)
                time.sleep(hold_time)
                self.keyboard_controller.release(key)

        elif action_type == 'pause':
            duration = action.get('duration', 1.0)
            print(f"Pausing for {duration}s")
            # Sleep in small chunks to allow immediate stopping
            end_time = time.time() + duration
            while time.time() < end_time and self.running:
                time.sleep(0.1)

    def run_actions(self):
        while self.program_running:
            if self.running:
                actions = self.config.get('actions', [])
                for action in actions:
                    if not self.running:
                        break
                    self.execute_action(action)
            else:
                time.sleep(0.1)

    def toggle(self):
        self.running = not self.running
        if self.running:
            print("AutoClicker STARTED")
            # Reload config on start to pick up changes
            self.load_config()
        else:
            print("AutoClicker STOPPED")

    def start(self):
        # Start the action loop in a separate thread
        action_thread = threading.Thread(target=self.run_actions)
        action_thread.daemon = True
        action_thread.start()

        # Setup hotkey listener
        hotkey_str = self.config.get('hotkey', '<f8>')
        
        listener = keyboard.GlobalHotKeys({
            hotkey_str: self.toggle
        })
        
        print(f"Listening for hotkey: {hotkey_str}")
        print("Press Ctrl+C to exit program")
        
        listener.start()

        try:
            while self.program_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            self.program_running = False
            listener.stop()
        except Exception as e:
            print(f"Error: {e}")
            self.program_running = False
            listener.stop()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Python Auto Clicker")
    parser.add_argument("config", nargs="?", default="config.json", help="Path to the configuration file (default: config.json)")
    args = parser.parse_args()

    clicker = AutoClicker(config_path=args.config)
    clicker.start()
