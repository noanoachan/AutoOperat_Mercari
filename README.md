## 環境構築手順(Mac版)　　

[1]　仮想環境作成(venv)　　
```
$ python3 -m venv "仮想環境名"　　
```

[2]　仮想環境をアクティブ　　
```
$ . "仮想環境名"/bin/activate　　
```

[3] 各パッケージのインストール　　
https://github.com/noanoachan/AutoOperat_Mercari/blob/main/venv_AutoOperat_Mercari/requirements.txt　　
```
$ pip install -r requirements.txt
```

## ビルド手順　　
[1]　仮想環境内直下に dat, doc, log, src フォルダを配置　　

[2]　doc/UserInfo.xml に自信のアカウント情報を登録

[3]　任意のテキストエディタでビルド　　

[※]初期動作の場合、二段階認証が求められるが手動にて対応（登録電話番号に届く6桁の認証コードを入力）  
[※]次回以降はログインキャッシュが生成されるので上記の対応は行わない　　


[不具合対応]
1. ログイン等で失敗した場合や何らかの不具合に合った時、dat/rm.command を実行する　　
2. dat/LoginCacheフォルダが消えていることを確認し、[3]を再度実行する　　

## その他　　
- dat, doc, logフォルダについて　　

ソースコード内にコメントを細かく残しているので使用方法等を要確認　　
