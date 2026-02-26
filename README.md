# Python Auto Clicker

A customizable, JSON-configured auto clicker with hotkey support.

## Installation

1.  **Install Python**: Ensure you have Python 3.x installed.
2.  **Install Dependencies**:
    Open a terminal in this folder and run:
    ```bash
    pip install pynput
    ```

## Configuration

Edit the `config.json` file to define your click sequence.

**Example `config.json`:**
```json
{
  "description": "My custom sequence",
  "hotkey": "<f8>",
  "actions": [
    { "type": "click", "button": "left", "hold_time": 3.0 },
    { "type": "pause", "duration": 2.0 },
    { "type": "click", "button": "right", "hold_time": 0.1 },
    { "type": "pause", "duration": 20.0 }
  ]
}
```

*   **description**: Optional. A short text describing what this config does.
*   **hotkey**: The key to start/stop the clicker (e.g., `<f8>`, `<ctrl>+<alt>+s`).
*   **actions**: A list of actions to perform in a loop.
    *   **click**: Simulates a mouse click.
        *   `button`: "left" or "right".
        *   `hold_time`: How long to hold the button down (seconds).
    *   **key_press**: Simulates a keyboard key press.
        *   `key`: The key to press (e.g., "a", "space", "enter", "shift").
        *   `hold_time`: How long to hold the key down (seconds).
    *   **pause**: Waits for a specified duration.
        *   `duration`: Time to wait (seconds).

## Usage

1.  Run the program:
    ```bash
    python clicker.py [config_file]
    ```
    *   `[config_file]`: Optional. Path to your JSON config file (defaults to `config.json`).
2.  Press the configured **hotkey** (default: F8) to START the clicker.
3.  Press the **hotkey** again to STOP the clicker.
4.  Press **Ctrl+C** in the terminal to exit the program completely.

> **Note**: The configuration is reloaded every time you start the clicker, so you can edit `config.json` while the script is running (just stop and start to apply changes).
