# -*- coding: utf-8 -*-
import base64

def qqdlLinkGenerator(link_: str):
    return "qqdl://" + str(base64.b64encode(link_.encode("utf-8")))[2:-1]


if __name__ == "__main__":
    pass
