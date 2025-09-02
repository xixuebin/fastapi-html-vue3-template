import yaml

def load_users():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("users", [])


def validate_user(username: str, password: str) -> bool:
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

