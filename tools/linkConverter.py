# -*- coding: utf-8 -*-
try:
    from .flashgetLinkGenerator import flashgetLinkGenerator
    from .flashgetLinkRestore import flashgetLinkRestore
    from .qqdlLinkGenerator import qqdlLinkGenerator
    from .qqdlLinkRestore import qqdlLinkRestore
    from .thunderLinkGenerator import thunderLinkGenerator
    from .thunderLinkRestore import thunderLinkRestore
except ImportError:
    from flashgetLinkGenerator import flashgetLinkGenerator
    from flashgetLinkRestore import flashgetLinkRestore
    from qqdlLinkGenerator import qqdlLinkGenerator
    from qqdlLinkRestore import qqdlLinkRestore
    from thunderLinkGenerator import thunderLinkGenerator
    from thunderLinkRestore import thunderLinkRestore

def linkConverter(link_):
    linkList = {}
    if link_.startswith("flashget://"):
        linkList["real"] = flashgetLinkRestore(link_)
    elif link_.startswith("qqdl://"):
        linkList["real"] = qqdlLinkRestore(link_)
    elif link_.startswith("thunder://"):
        linkList["real"] = thunderLinkRestore(link_)
    else:
        linkList["real"] = link_
    linkList["flashget"] = flashgetLinkGenerator(linkList["real"])
    linkList["qqdl"] = qqdlLinkGenerator(linkList["real"])
    linkList["thunder"] = thunderLinkGenerator(linkList["real"])
    return linkList


if __name__ == "__main__":
    pass
