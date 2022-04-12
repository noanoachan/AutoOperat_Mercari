import sys
from tkinter import messagebox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from telnetlib import EC
from bs4 import BeautifulSoup
import lxml
import re
import time
import random
import os
import time
import Const
import ProductInfo
import Log


class CrawlingBrowser():
    """
    Class:
        ブラウザのクロールクラス
    """
    __m_strUrl = ''
    
    def __init__(self, strUrl):
        """
        Details:
            コンストラクタ
        Param:
            strUrl    対象URL
        """
        self.__m_strUrl = strUrl
        
    
    def loginMercari(self, driver, objUserInfo):
        """
        Details:
            メルカリログイン
        Param:
            driver          ドライバー
            objUserInfo     ユーザー情報
        Return:
            driver  2段階認証突破後のドライバー
        """
        logging = Log.getLogger()
        
        objCssSelectorConst = Const.CssSelector
        
        # 要素が表示されるまでの待機処理
        wait = WebDriverWait(driver, 20)
        # ランダムな秒数処理を停止（自動化を誤魔化す処理 2s~7s）
        waitsec=random.randint(1,3)
        
        try:
            # メルカリを開く
            driver.get(self.__m_strUrl)
            time.sleep(waitsec)
            
            # ログインキャッシュの有無
            if not objUserInfo.getExistCache():
                # ログイン
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_LOGIN)))
                driver.find_element_by_css_selector(objCssSelectorConst.BTN_LOGIN).click()
                # メールアドレスでログイン
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_MAIL_ADDRESS_LOGIN)))
                driver.find_element_by_css_selector(objCssSelectorConst.BTN_MAIL_ADDRESS_LOGIN).click()
                
                time.sleep(waitsec)
                
                # ユーザー情報入力
                wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
                elmEmail = driver.find_element_by_name('email')
                elmEmail.send_keys(objUserInfo.getEmail())
                
                wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
                elmPass = driver.find_element_by_name('password')
                elmPass.send_keys(objUserInfo.getPass())
                
                # ログイン実行
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_LOGIN_EXECUTION)))
                driver.find_element_by_css_selector(objCssSelectorConst.BTN_LOGIN_EXECUTION).click()
                
                # 初回2段階認証は手動対応
                MERCARI_HOME = 'https://jp.mercari.com/'
                strCurrentURL = driver.current_url
                
                # 現在のURLを取得し、変更されたら突破したと解釈しループを抜ける
                nWaitCount = 0
                while strCurrentURL != MERCARI_HOME:
                    time.sleep(2)
                    strCurrentURL = driver.current_url
                    
                    # 1分間、2段階認証が突破される事を待つ
                    nWaitCount += 1
                    if nWaitCount == 30:
                        logging.critical('timeout：2段階認証コードの入力が確認できませんでした')
                        raise
        except Exception as e:
            logging.critical('ログインに失敗しました')
            print(f'ExceptionLog : {e}')
            sys.exit()
    
    
    
    def getListingList(self, driver):
        """
        Details:
            出品商品の取得
        Return:
            lstListingProduct   出品商品のリスト
        """
        logging = Log.getLogger()
        
        objCssSelectorConst = Const.CssSelector
        objXpath = Const.Xpath
        
        # 要素が表示されるまでの待機処理
        wait = WebDriverWait(driver, 20)
        
        try:
            # アカウント
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_ACCOUNT)))
            driver.find_element_by_css_selector(objCssSelectorConst.BTN_ACCOUNT).click()
            time.sleep(random.randint(1,3))
            
            # 出品した商品
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_LISTED_ITEM)))
            driver.find_element_by_css_selector(objCssSelectorConst.BTN_LISTED_ITEM).click()
            time.sleep(random.randint(1,3))
            
            # もっと見る
            blChecl = True
            while blChecl:
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, objXpath.BTN_SEE_MORE)))
                    driver.find_element_by_xpath(objXpath.BTN_SEE_MORE).click()
                    time.sleep(random.randint(2,4))
                except:
                    #「もっと見る」要素がなくなるまでループさせる
                    blChecl = False
                    pass
            
            # 商品名の取得
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.LST_PRODUCT)))
            objProductInfoList = driver.find_elements_by_css_selector(objCssSelectorConst.LST_PRODUCT)
            logging.info('全ての商品名を取得しました')

            # 商品URLの取得
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            lstProductUrls = soup.find_all(href=re.compile('/item/m'))
            logging.info('全て商品URLを取得しました')
            
            
        except Exception as e:
            logging.critical('商品情報の取得中にエラーが発生しました。')
            print(f'ExceptionLog : {e}')
            raise
                

        lstListingProduct = []
        for count in range(len(objProductInfoList)):
            # 商品名の整形
            strProductName = (objProductInfoList[count].text).split('\n')[0]
            # 商品IDの整形
            strProductId = (lstProductUrls[count].get('href')).split('/')[-1]
            # 商品URLの整形
            strProductUrl = self.__m_strUrl + lstProductUrls[count].get('href')
                
            if strProductName != '' and strProductId != '':
                objListingProduct = ProductInfo.ListingProduct(strProductName, strProductId)
                objListingProduct.setProductUrl(strProductUrl)
                lstListingProduct.append(objListingProduct)
            else:
                logging.error(f'{count}目の出品商品情報の取得に失敗しました。')
                pass
            
        return lstListingProduct
    
    
    def exePriceCut(self, driver, objPriceCutProduct):
        """
        Details:
            商品の値下げ実行
        Param:
            driver              ドライバー
        Param:
            objPriceCutProduct  値下げ商品情報
        """
        logging = Log.getLogger()
        
        objCssSelectorConst = Const.CssSelector
        objClassName = Const.ClassName
        
        # 要素が表示されるまでの待機処理
        wait = WebDriverWait(driver, 20)
        
        
        # 出品中の商品情報
        strProductName  = objPriceCutProduct.getProductName()
        strProductId    = objPriceCutProduct.getProductId()
        objListingProduct = ProductInfo.ListingProduct(strProductName, strProductId)
        
        try:
            # 各商品ページ
            strProductUrl = f'https://jp.mercari.com/item/{objPriceCutProduct.getProductId()}'
            objListingProduct.setProductUrl(strProductUrl)
            driver.get(strProductUrl)
            time.sleep(random.randint(2,5))
            
            # Web情報の取得（商品ページ）
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            
            time.sleep(random.randint(2,5))
            
            # 商品情報の要素に「公開停止」状態の要素が含まれていたら終了
            lstStopPublishing = soup.find_all(text=re.compile("公開停止中"))
            if len(lstStopPublishing) > 0:
                objListingProduct.setProductStopPublishing(True)
                
                logging.warning(f'商品状態が「公開停止」です。商品ID［{objPriceCutProduct.getProductId()}］')
                return objListingProduct
            
            # 商品情報の要素に「削除」状態の要素が含まれていたら終了
            lstProductDelete = soup.find_all(text=re.compile("ページが見つかりませんでした"))
            if len(lstProductDelete) > 0:
                objListingProduct.setProductDelete(True)
                
                logging.warning(f'商品が削除されている可能性があります。商品ID［{objPriceCutProduct.getProductId()}］')
                return objListingProduct
            
            # 商品情報の要素に「売り切れ」状態の要素が含まれていたら終了
            lstSoldOut = soup.find_all(text=re.compile("売り切れ"))
            if len(lstSoldOut) > 0:
                objListingProduct.setProductSoldOut(True)
                
                logging.warning(f'商品は既に売り切れています。商品ID［{objPriceCutProduct.getProductId()}］')
                return objListingProduct
            
            
            time.sleep(random.randint(2,5))
            
            # 出品価格取得
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.ELEM_PRICE)))
            strPrice = driver.find_elements_by_css_selector(objCssSelectorConst.ELEM_PRICE)[0].text
            lstNumber = strPrice.split(',')
            
            # 出品価格の値が文字列なので数値に変換後'¥'を削除
            strSubPrice = ''
            for count in range(len(lstNumber)):
                strSubPrice += lstNumber[count]            
            strSubPrice = strSubPrice.lstrip('¥')
            nPrice = int(strSubPrice)
            
            # 予め設定された最安値価格より現在の出品価格が低ければ値下げを行わない
            if nPrice <= objPriceCutProduct.getCheapestPrice():
                logging.info('設定された価格より現在の価格が下回るのでパスしました。')
                logging.debug(f'商品ID［{objPriceCutProduct.getProductId()}］：現在の出品価格［{nPrice}円］< 最安値設定価格［{objPriceCutProduct.getCheapestPrice()}円］')
                time.sleep(random.randint(2,5))
                
                return objListingProduct
            
            
            # 商品の編集
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_PRODUCT_EDIT)))
            driver.find_element_by_css_selector(objCssSelectorConst.BTN_PRODUCT_EDIT).click()
            
            # 販売価格の要素を取得
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, objClassName.INPUT_SELL_PRICE)))
            driver.find_element_by_class_name(objClassName.INPUT_SELL_PRICE).click()
            
            # 現在設定されている販売価格をクリア ↓※clear関数が使用できない時の対処法
            # WindowsOS/MacOS で、入力キーが異なる
            if os.name == 'nt':
                driver.find_element_by_class_name(objClassName.INPUT_SELL_PRICE).send_keys(Keys.CONTROL + "a")
            elif os.name == 'posix':
                driver.find_element_by_class_name(objClassName.INPUT_SELL_PRICE).send_keys(Keys.COMMAND + "a")
            
            driver.find_element_by_class_name(objClassName.INPUT_SELL_PRICE).send_keys(Keys.DELETE)
            driver.find_element_by_class_name(objClassName.INPUT_SELL_PRICE).clear()
            
            # 現在の販売価格から値下げ価格を減算
            nSettingPrice = nPrice - objPriceCutProduct.getPriceCut()
            # 設定された値下げ価格へ変更
            driver.find_element_by_class_name(objClassName.INPUT_SELL_PRICE).send_keys(nSettingPrice)
            
            time.sleep(random.randint(2,5))
            
            # 変更を適応して終了
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, objCssSelectorConst.BTN_CHANGED)))
            driver.find_element_by_css_selector(objCssSelectorConst.BTN_CHANGED).click()
            
            time.sleep(random.randint(2,5))
            logging.info(f'商品ID［{objPriceCutProduct.getProductId()}］を［{objPriceCutProduct.getPriceCut()}円］値下げしました')
            
            return objListingProduct
            
        except Exception as e:
            logging.error(f'値下げ中にエラーが発生しました。商品ID={objPriceCutProduct.getProductId()}')
            print(f'ExceptionLog : {e}')
            time.sleep(random.randint(2,5))
            return objListingProduct