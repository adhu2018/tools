# -*- coding: utf-8 -*-
import base64

def thunderLinkGenerator(link_: str):
    return "thunder://" + str(base64.b64encode(f"AA{link_}ZZ".encode("utf-8")))[2:-1]


if __name__ == "__main__":
    pass
