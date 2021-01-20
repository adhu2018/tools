# -*- coding: utf-8 -*-
import hashlib

# md5(str[, encoding]) or md5(bytes) or md5(int)
def md5(*_str):
    if len(_str) > 0:
        t = _str[0]
        if type(t) is not str:
            t = str(t)
        encode_type = "utf-8"
        if len(_str) > 1:
            encode_type = _str[1]
        m = hashlib.md5()
        try:
            t = t.encode(encode_type)
        except LookupError:
            t = t.encode("utf-8")
        m.update(t)
        return m.hexdigest()
    else:
        print("缺少参数！")
        return False


if __name__ == "__main__":
    pass
