import os
import sys
import xml.etree.ElementTree as ET
import Log


class UserInfo:
    """    
    Class:
        ユーザー情報クラス
    """
    __instance  = None      # シングルトン
    
    __m_strEmail = ''       # メールアドレス
    __m_strPass = ''        # パスワード
    __m_blCache = False     # キャッシュ情報
    
    def __new__(cls):
        """
        Details:
            シングルトン
        Returns:
            UserInfo
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            
        return cls.__instance
    
    @staticmethod
    def getInstance():
        """
        Details:
            インスタンスの取得
        Return:
            UserInfo        インスタンス
        """
        return UserInfo.__instance
    
            
    def setEmail(self, strEmail: str):
        """
        Details:
            メールアドレスの設定
        Param:
            __m_strEmail    メールアドレス
        """
        self.__m_strEmail = strEmail
        
    def setPass(self, strPass: str):
        """        
        Details:
            パスワードの設定
        Param:
            __m_strPass     パスワード
        """
        self.__m_strPass = strPass
        
    def setExistCache(self, strExistCache: bool):
        """        
        Details:
            ログインキャッシュの有無
        Param:
            __m_blCache     キャッシュ情報
        """
        self.__m_blCache = strExistCache
        
        
    #################################################
    
    
    def getEmail(self) -> str:
        """
        Details:
            メールアドレスの取得
        Return:
            __m_strEmail    メールアドレス
        """
        return self.__m_strEmail
    
    def getPass(self) -> str:
        """
        Details:
            パスワードの取得
        Return:
            __m_strPass     パスワード
        """
        return self.__m_strPass
    
    def getExistCache(self) -> bool:
        """
        Details:
            ログインキャッシュの有無を取得
        Return:
            __m_blCache     キャッシュ情報
        """
        return self.__m_blCache
    
    
class ReadUserInfo:
    """    
    Class:
        アカウント情報の読み取り
    """

    def readUserInfo(self, objUserInfo):
        """        
        Details:
            ユーザー情報の取得
        Param:
            objUserInfo     ユーザー情報
        Return:
            blRet   True:成功 / False:失敗
        """
        logging = Log.getLogger()
        
        try:
            baseFilePath = os.path.dirname(os.path.abspath(sys.argv[0]))    # ×：__file__  / ○：sys.argv[0]
            tree = ET.parse(os.path.normpath(os.path.join(baseFilePath, r'..\doc\UserInfo.xml')))
            root = tree.getroot()
            for userInfo in root.findall('UserInfo'):
                objUserInfo.setEmail(userInfo.find('Email').text)
                objUserInfo.setPass(userInfo.find('Pass').text)
            
            if objUserInfo.getEmail() == '' or objUserInfo.getPass() == '':
                logging.error('各要素が空です。（.xmlに適切な情報を入力して下さい）')
                exit()
                
        except Exception as e:
            logging.critical('.xmlの取得に失敗しました。')
            print(e)
            exit()

        logging.info('ログイン情報の取得に成功しました。')
