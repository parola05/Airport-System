from UI import UI
from Conf import Conf
import json

if __name__ == "__main__":
    with open('conf.json') as f:
        conf = json.load(f)
    Conf.initialize(
        openfireServer=conf["openfireServer"],
        openfirePassword=conf["openfirePassword"]
    )
    print(Conf().get_openfire_server())
    print(Conf().get_openfire_password())
    ui = UI()
    ui.start()