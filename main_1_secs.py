import os
from syftbox.lib import ClientConfig

# the name of the app is the name of the folder this is in
app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

client_config = ClientConfig.load(
    os.path.expanduser("~/.syftbox/client_config.json")
)
