import json
import os


def load_json(file_path, default):
    if not os.path.exists(file_path):
        save_json(file_path, default)
        return default

    try:
        with open(file_path, "r") as f:
            content = f.read().strip()

            if not content:
                save_json(file_path, default)
                return default

            return json.loads(content)

    except Exception:
        save_json(file_path, default)
        return default


def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)