class CssSelector:
    """
    Class:
        クローリング時の css_selector
    """
    # ログイン
    BTN_LOGIN = '#gatsby-focus-wrapper > div > div > header > mer-navigation-top > nav > mer-navigation-top-menu > mer-navigation-top-menu-item:nth-child(2) > span'
    # メールアドレスでログイン
    BTN_MAIL_ADDRESS_LOGIN = '#root > div > div > div > main > div > div > div > div > mer-button.style_loginButton__1-1k6.mer-spacing-b-24.style_email__1PIYq > a'
    # ログイン実行
    BTN_LOGIN_EXECUTION = '#root > div > div > div > main > div > div > form > mer-button > button'
    # 認証して完了する
    BTN_TWO_STEP_VERIFICATION = '#root > div > div > div > main > div > div > div > div.sc-hHEiqL.YzGzU > form > mer-button > button'
    
    # アカウント
    BTN_ACCOUNT = '#gatsby-focus-wrapper > div > div > header > mer-navigation-top > nav > mer-navigation-top-menu > mer-menu > mer-navigation-top-menu-item > span'
    # 出品した商品
    BTN_LISTED_ITEM = '#gatsby-focus-wrapper > div > div > header > mer-navigation-top > nav > mer-navigation-top-menu > mer-menu > div > mer-list > mer-list-item:nth-child(4) > a'
    
    # 商品リスト
    LST_PRODUCT = '#currentListing > mer-list mer-list-item'
    
    # 出品価格
    # (旧) ELEM_PRICE = '#item-info > section:nth-child(1) > section:nth-child(2) > mer-text > mer-price'
    ELEM_PRICE = '#item-info > section:nth-child(1) > section:nth-child(2) > div > mer-price'
    
    # 商品の編集
    BTN_PRODUCT_EDIT = '#item-info > section:nth-child(1) > div:nth-child(5) > mer-button > a'
    
    # 変更する
    BTN_CHANGED = '#main > form > div.layout__FlexWrapper-sc-1lyi7xi-9.eNrnaj > mer-button:nth-child(1) > button'
    
    
class ClassName:
    """
    Class:
        クローリング時の class_name
    """
    # 販売価格
    INPUT_SELL_PRICE = 'input-node.no-spin-button.with-prefix-label'
    
    
class Xpath:
    """
    class:
        クローリング時の Xpath
    """
    # もっと見る
    BTN_SEE_MORE = '//*[@id="currentListing"]/div/mer-button/button'
    
    # 商品リスト中の価格
    ELEM_LIST_ON_PRICE = '//*[@id="currentListing"]/mer-list/mer-list-item[1]/a/mer-item-object//div/div/div[1]/mer-text/mer-price//span[2]'
    
class CellData:
    """
    Class:

    """
    PRODUCT_NAME    = 0     # 商品名
    PRODUCT_ID      = 1     # 商品ID
    CHEAPES_PRICE   = 2     # 最安値
    REMARKS         = 3     # 備考