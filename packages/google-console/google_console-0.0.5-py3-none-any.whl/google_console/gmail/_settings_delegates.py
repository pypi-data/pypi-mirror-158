from .._pipeline import Base
from typing import List, Union


# SETTINGS DELEGATES
class SettingsDelegates(Base):
    
    def __init__(self, client_secret_file: str, api_version: str, recreate_service: bool = False,
                 prefix: str = "", suffix: str = "", token_dir: str = ""):
        scopes = []
        super(SettingsDelegates, self).__init__("gmail", client_secret_file, api_version,
                                                scopes, recreate_service, prefix, suffix, token_dir)
    
    def create(self):
        pass
    
    def get(self):
        pass
    
    def list(self):
        pass
