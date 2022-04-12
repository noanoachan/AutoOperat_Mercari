class Product():
    """
    Class:
        商品情報
    """
    m_strProductName = ''    # 商品名
    m_strProductId   = ''    # 商品ID
    m_strProductUrl  = ''    # 商品URL
    
    def __init__(self, strProductName, strProductId):
        """
        Details:
            コンストラクタ
        Args:
            strProductName      商品名
            strProductId        商品ID
        """
        self.m_strProductName   = strProductName
        self.m_strProductId     = strProductId            

    
    def getProductName(self):
        """
        Details:
            商品名の取得
        Return:
            strProductName  商品名
        """
        return self.m_strProductName

    def getProductId(self):
        """
        Details:
            商品IDの取得
        Return:
            strProductID  商品ID
        """
        return self.m_strProductId
    
    def getProductUrl(self):
        """
        Details:
            商品URLの取得
        Return:
            strProductURL  商品URL
        """
        return self.m_strProductUrl
        
        
    def setProductUrl(self, strProductUrl):
        """
        Details:
            商品URLの設定
        Args:
            strProductUrl               商品URL
        """
        self.m_strProductUrl = strProductUrl
    
    
class ListingProduct(Product):
    """
    Class:
        出品中の商品情報
    """
    m_blProductStopPublishing   = False     # 公開停止
    m_blProductDelete           = False     # 削除
    m_blProductSoldOut          = False     # 売り切れ  
    
    
    def getProductStopPublishing(self):
        """
        Details:
            公開停止ステータスの取得
        """
        return self.m_blProductStopPublishing
    
    def getProductDelete(self):
        """
        Details:
            削除ステータスの取得
        """
        return self.m_blProductDelete
    
    def getProductSoldOut(self):
        """
        Details:
            売り切れ状態の取得
        """
        return self.m_blProductSoldOut
    
    
        
    def setProductStopPublishing(self, blProductStopPublishing):
        """
        Details:
            公開停止状態の設定
        Args:
            blProductStopPublishing     公開停止状態
        """
        self.m_blProductStopPublishing = blProductStopPublishing
    
    def setProductDelete(self, blProductDelete):
        """
        Details:
            削除状態の設定
        Args:
            blProductDelete             削除状態
        """
        self.m_blProductDelete = blProductDelete
        
    def setProductSoldOut(self, blProductSoldOut):
        """
        Details:
            売り切れ状態の設定
        Args:
            blProductSoldOut            売り切れ状態
        """
        self.m_blProductSoldOut = blProductSoldOut
    
    
    
class PriceCutProduct(Product):
    """
    Class:
        値下げ商品情報
    """
    m_nPriceCut         = 100       # 値下げ価格（固定値：100円）
    m_nCheapestPrice    = 0         # 最安値の設定値
    
    
    def getPriceCut(self):
        """
        Details:
            値下げ価格の取得
        """
        return self.m_nPriceCut
    
    def getCheapestPrice(self):
        """
        Details:
            最安値の取得
        """
        return self.m_nCheapestPrice
    
    
    def setPriceCut(self, nPriceCut):
        """
        Details:
            値下げ価格の設定
        Args:
            nPriceCut           値下げ価格
        """
        self.m_nPriceCut = nPriceCut
    
    def setCheapestPrice(self, nCheapestPrice):
        """
        Details:
            最安値の設定
        Args:
            nCheapestPrice      最安値
        Return:
            blRet               True:成功/False:失敗
        """
        blRet = True
        
        if nCheapestPrice != 0:
            self.m_nCheapestPrice = nCheapestPrice
        else:
            blRet = False
            
        return blRet