# -*- coding: utf-8 -*-
import win32com.client

# 文本转语音，win10测试可行
def text2Speech(text):
    try:
        # Microsoft Speech API
        speak = win32com.client.Dispatch("SAPI.SpVoice")
        speak.Speak(text)
    except (ImportError, ModuleNotFoundError) as err:
        raise err


if __name__ == "__main__":
    pass
