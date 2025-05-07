import yaml

class GlobalConfig:
    _instance = None  # Singleton instance
    
    def __new__(cls, config_path="config.yaml"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config(config_path)
        return cls._instance
    
    def load_config(self, config_path):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, default)
        return value

CONFIG = GlobalConfig("config.yaml")
# Usage: Create a single instance for entire project
# CONFIG = GlobalConfig("config.yaml")
# print(CONFIG.get("data_paths.raw_data"))  # Access values anywhere
