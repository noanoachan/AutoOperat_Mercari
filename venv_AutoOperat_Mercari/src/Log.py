import logging
import sys
import os
import datetime

def getLogger():
    return Logger

# ログ出力先
strDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
baseFilePath = os.path.dirname(os.path.abspath(sys.argv[0]))    # ×：__file__  / ○：sys.argv[0]
strFilePath = os.path.normpath(os.path.join(baseFilePath, f'../log/{strDateTime}.log'))

Logger = logging.getLogger(__name__)
Logger.setLevel(logging.DEBUG)

Handler = logging.FileHandler(strFilePath)
Handler.setLevel(logging.DEBUG)

Fomatter = logging.Formatter('%(asctime)s - [%(levelname)s] : %(message)s [ファイル名=%(filename)s / 関数名=%(funcName)s 行=%(lineno)s]')
Handler.setFormatter(Fomatter)

Logger.addHandler(Handler)


