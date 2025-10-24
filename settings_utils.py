import json
import os

STATE_FILE = "app_state.json"

DEFAULT_STATE = {
    "settings": {
        "wallpaper": "ScreenPhoto2-2560x1440px.png"
    },
    "desktop_icons": []
}

def load_state():
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception as e:
            print(f"[WARNING] Failed to load state: {e}")
            state = {}

    merged = DEFAULT_STATE.copy()
    merged.update(state)
    if "settings" not in merged:
        merged["settings"] = DEFAULT_STATE["settings"].copy()

    wallpaper = merged["settings"].get("wallpaper", DEFAULT_STATE["settings"]["wallpaper"])
    if not wallpaper or not os.path.exists(wallpaper):
        print(f"[INFO] Wallpaper missing or invalid, resetting to default")
        merged["settings"]["wallpaper"] = DEFAULT_STATE["settings"]["wallpaper"]

    save_state(merged)
    return merged


def save_state(state: dict):
    try:
        folder = os.path.dirname(STATE_FILE)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print("[INFO] State saved successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to save state: {e}")