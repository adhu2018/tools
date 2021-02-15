# -*- coding: utf-8 -*-
import base64

def flashgetLinkGenerator(link_: str):
    return "flashget://" + str(base64.b64encode(f"[FLASHGET]{link_}[FLASHGET]".encode("utf-8")))[2:-1]

if __name__ == "__main__":
    pass
