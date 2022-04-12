from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import tkinter
import tkinter.ttk as ttk
from enum import Enum
import os
import sys
import ProductDataFile
import UserInfo
import CrawlingBrowser
import Log


class Operat(Enum):
    """
    Details:
        操作項目
    """
    GetGata     = 'データ取得'      # データ取得
    PriceCut    = '値下げ実行'      # 値下げ実行
    Other       = 'その他'          # その他
    

def exeOperat(event):
    """
    Details:
                選択項目の実行
    Param:
        event   イベント
    """
    logging = Log.getLogger()
    
    try:
        # データ取得
        if strOpeartElement.get() == Operat.GetGata.value:
            logging.info(f'【{Operat.GetGata.value}】が選択されました')
            main(Operat.GetGata)
            
        # 値下げ実行
        elif strOpeartElement.get() == Operat.PriceCut.value:
            logging.info(f'【{Operat.PriceCut.value}】が選択されました')
            main(Operat.PriceCut)
    
    
        logging.info(f'【{Operat.GetGata.value}】が完了しました')    
    
    except Exception as e:
        logging.error(f'【{strOpeartElement.get()}】の処理中にエラーが発生しました')
        print(f'{e}')
        strLabelText.set(f'エラーが発生しました。再度実行して下さい。')
        
    # ループ
    guiWindow.mainloop()
    


def selectComboBox(event):
    """
    Details:
                操作項目の選択値をラベルへ反映
    Param:
        event   イベント
    """
    logging = Log.getLogger()
    
    # 選択項目の表示（ラベル）
    strLabelText.set(f'{strOpeartElement.get()}中...')
    
    # その他
    if strOpeartElement.get() == Operat.Other.value:
        strLabelText.set('選択して下さい')
        logging.warning(f'【{Operat.Other.value}】が選択されました')
        
    
    
def guiOperat():
    """
    Details:
                GUIウィンドウの表示
    """    
    # 操作画面表示
    lstOpeartElement = []
    lstOpeartElement.append(Operat.GetGata.value)     # データ取得
    lstOpeartElement.append(Operat.PriceCut.value)    # 値下げ実行
    
    # GUI
    # ウィンドウの作成
    global guiWindow
    guiWindow = tkinter.Tk()
    guiWindow.title('コントロール画面')
    #（横 × 高さ + x座標 + y座標）
    guiWindow.geometry('600x400+500+500')
    
    # フレームの作成
    nFrameWidth = 550
    nFrameHeight = 375
    guiFrame = tkinter.Frame(guiWindow, width=nFrameWidth, height=nFrameHeight, background='#808080')
    guiFrame.place(x=(600-nFrameWidth)/2, y=(400-nFrameHeight)/2)
    
    # コンボボックス
    nComboBoxWidth = 200
    global strOpeartElement
    strOpeartElement = tkinter.StringVar()
    combobox = ttk.Combobox(guiFrame, width=20, height=2, state="readonly", textvariable=strOpeartElement, values=lstOpeartElement)
    combobox.place(width=nComboBoxWidth, x=(nFrameWidth-nComboBoxWidth)/2, rely=0.1)
    
    # 選択ボタン
    nButtonWidth = 200
    button = tkinter.Button(guiFrame, text='選択', width=20, height=4)
    button.bind('<ButtonPress>', selectComboBox)
    button.place(width=nButtonWidth, x=(nFrameWidth-nButtonWidth)/2, rely=0.3)
    
    # ラベル
    global strLabelText
    strLabelText = tkinter.StringVar()
    strLabelText.set('項目を選択中...')
    global label
    label = tkinter.Label(guiFrame, text=strLabelText.get(), textvariable=strLabelText, background='#000', foreground='#FFF')
    label.place(width=nButtonWidth, x=(nFrameWidth-nButtonWidth)/2, rely=0.55)
    
    # 実行ボタン
    button = tkinter.Button(guiFrame, text='実行', width=20, height=4)
    button.bind('<ButtonPress>', exeOperat)
    button.place(width=nButtonWidth, x=(nFrameWidth-nButtonWidth)/2, rely=0.65)
        
    guiWindow.mainloop()
    
    
    
def main(valOperat):
    """
    Details:
                    main関数
    Param:
        valOperat   操作対象（データ取得、値下げ実行、その他）
    """
    logging = Log.getLogger()
    MERCARI_HOME = 'https://jp.mercari.com/'
    
    # ユーザー情報クラス
    objUserInfo = UserInfo.UserInfo()
    
    # ログインキャッシュの確認と再び Webへアクセスしないための制限
    if not objUserInfo.getExistCache():
        try:
            # ログインキャッシュの有無
            baseFilePath = os.path.dirname(os.path.abspath(sys.argv[0]))    # ×：__file__  / ○：sys.argv[0]
            strLoginChace_dir = os.path.normpath(os.path.join(baseFilePath, r'..\dat\LoginCache'))
            
            # オプション設定
            options = webdriver.ChromeOptions()
            # ログインキャッシュが存在するか否か
            if not os.path.exists(strLoginChace_dir):
                os.makedirs(strLoginChace_dir, exist_ok=True)
                options.add_argument(f'--user-data-dir={strLoginChace_dir}')
                logging.info('ログインキャッシュを生成しました')
                
            else:
                options.add_argument(f'--user-data-dir={strLoginChace_dir}')
                logging.info('ログインキャッシュが確認できました')
                
            
            # ログインキャッシュの有無を「有」へ変更
            objUserInfo.setExistCache(True)
            
            # 環境に応じた webdriverを自動インストール
            global DRIVER
            DRIVER = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
            
            # .xml：アカウント情報の取得 
            objReadUserInfo = UserInfo.ReadUserInfo()
            objReadUserInfo.readUserInfo(objUserInfo)
        
        
        except Exception as e:
            logging.critical('ログインキャッシュ情報確認中に致命的なエラーが発生しました')
            logging.critical('続行不可能なため終了します')
            print(f'{e}')
            
            # 終了
            sys.exit()
        
    
    # .xlsx：値下げ商品クラス
    objReadData = ProductDataFile.ReadData()
    
    # ログイン
    url = 'https://jp.mercari.com/'
    objCrawlingBrowser = CrawlingBrowser.CrawlingBrowser(url)
    objCrawlingBrowser.loginMercari(DRIVER, objUserInfo)
    
    
    try:
        ################################################################################################
        ### データ取得
        ################################################################################################
        if valOperat == Operat.GetGata:
            # 出品中の商品情報の取得（商品名、商品ID、商品URL）
            lstListingProduct = []
            lstListingProduct = objCrawlingBrowser.getListingList(DRIVER)
            logging.info('出品中の全ての商品情報の取得が完了しました')
            
            # 値下げ商品情報の取得（商品名、商品ID、最安値）
            lstPriceCutProduct = []
            objReadData.readPriceCutProduct(lstPriceCutProduct)
            logging.info('登録されてある商品情報の取得が完了しました')
            
            # 記録対象の出品中商品情報
            lstWriteProductInfo = []
            for objListingProduct in lstListingProduct:
                # 商品情報ファイルに商品が1つも登録されていなければ全て追加
                if  len(lstPriceCutProduct) == 0:
                    lstWriteProductInfo.append(objListingProduct)
                    logging.info(f'登録商品情報にデータがありませんでしたので新規追加します。商品ID：{objListingProduct.getProductId()}')
                
                else:
                    # 商品情報ファイルに登録されてある商品リスト
                    for objPriceCutProduct in lstPriceCutProduct:
                        
                        # 一致すれば次の出品中の商品情報へ
                        if objListingProduct.getProductId() == objPriceCutProduct.getProductId():
                            break
                        
                        # 最後の商品情報に到達すれば追加
                        elif objPriceCutProduct.getProductId() == lstPriceCutProduct[-1].getProductId():
                            lstWriteProductInfo.append(objListingProduct)
                            logging.info(f'登録商品情報にデータがありませんでしたので新規追加します。商品ID：{objListingProduct.getProductId()}')
                            
                        # 一致しなければ次の商品情報へ
                        elif objListingProduct.getProductId() != objPriceCutProduct.getProductId():
                            continue
            
            # データファイルへ書き込み
            objWriteData = ProductDataFile.WriteData()
            objWriteData.writeProductInfo(lstWriteProductInfo)
            
            
            # 初期化
            lstListingProduct   = []    # 出品中の商品情報
            lstPriceCutProduct  = []    # 商品情報のデータファイル情報
            lstWriteProductInfo = []    # 記録用の出品中商品情報
            
            DRIVER.get(MERCARI_HOME)
        
        ################################################################################################
        ### 値下げ実行
        ################################################################################################
        elif valOperat == Operat.PriceCut:
            # 値下げ商品情報の取得（商品名、商品ID、最安値）
            lstPriceCutProduct = []
            objReadData.readPriceCutProduct(lstPriceCutProduct)
            logging.info('登録されてある商品情報の取得が完了しました')
            
            # 上記で抽出した商品情報を元に値下げを実行
            lstWriteProductStatus = []
            for objPriceCutProduct in lstPriceCutProduct:
                # 値下げ実行時に取得した商品情報を取得
                objListingProduct = objCrawlingBrowser.exePriceCut(DRIVER, objPriceCutProduct)
                lstWriteProductStatus.append(objListingProduct)
            
            # データファイルへ書き込み
            objWriteData = ProductDataFile.WriteData()
            objWriteData.writeProductStatus(lstWriteProductStatus)
            
            
            # 初期化
            lstPriceCutProduct      = []
            lstWriteProductStatus   = []
            
            DRIVER.get(MERCARI_HOME)
            
            
        ################################################################################################
        ### その他
        ################################################################################################
        elif valOperat == Operat.Other:
            logging.info('未実装：その他')
          
          
        ################################################################################################
        ### None
        ################################################################################################
        else:
            logging.info('未実装：None')
            
        
        logging.info(f'{valOperat.value}：データを初期化しました')
        # 選択項目の完了表示（ラベル）
        strLabelText.set(f'{strOpeartElement.get()}が完了しました')
        
    except:
        raise
        
    # GUI操作へ
    label['text'] = (f'次の操作を選択して下さい\n前回の操作【{valOperat.value}】')
    guiWindow.mainloop()
    
    
    
if __name__ == '__main__':
    # GUI操作画面
    guiOperat()
