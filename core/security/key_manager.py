import os

class KeyManager:
    def __init__(self):
        pass

    def set_key(self, service: str, key: str):
        # In a real app, use system keyring
        # For now, we simulate or store in env var for the session
        os.environ[f"RECALL_KEY_{service.upper()}"] = key

    def get_key(self, service: str) -> str:
        return os.environ.get(f"RECALL_KEY_{service.upper()}")

    def delete_key(self, service: str):
        env_key = f"RECALL_KEY_{service.upper()}"
        if env_key in os.environ:
            del os.environ[env_key]
