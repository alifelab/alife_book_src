# 作って動かす ALife - 実装を通した人工生命モデル入門

本リポジトリはオライリー・ジャパン発行書籍『[作って動かす ALife](https://www.oreilly.co.jp/books/9784873118475/)』のサポートサイトです。

* 書籍内に誤植などを見つけた方はこちら &rarr; [正誤表](https://github.com/alifelab/alife_book_src/wiki/%E6%AD%A3%E8%AA%A4%E8%A1%A8)

* プログラムの動作がおかしい/バグを発見した場合はこちら &rarr; [バグ報告](https://github.com/alifelab/alife_book_src/wiki/%E3%83%90%E3%82%B0%E5%A0%B1%E5%91%8A)

* サンプルプログラムの変更履歴はこちら &rarr; [変更履歴](https://github.com/alifelab/alife_book_src/wiki/%E5%A4%89%E6%9B%B4%E5%B1%A5%E6%AD%B4)

![表紙](https://user-images.githubusercontent.com/1583412/43062946-5a31d5b8-8e95-11e8-802a-53d2e58dc93e.jpeg)

---

## ファイル構成

|フォルダ名 |説明                         |
|:--        |:--                          |
|chap02       |2章で使用するソースコード    |
|chap03       |3章で使用するソースコード    |
|...        |...                          |
|chap06_07       |6,7章で使用するソースコード    |
|alifebook_lib   |各章で利用するユーティリティライブラリ  |


ソースコードの解説は本書をご覧ください。

## 必要条件
ソースコードの実行環境と必要なパッケージは以下です。

本書全体

* Python 3.6.3
* NumPy  1.14.5
* Vispy  0.5.3
* PyQt  5.10.1

5章
* Pyglet 1.3.2
* Pymunk  5.3.2

6章および7章

* Pillow  5.1.0
* Keras  2.2.0
* TensorFlow  1.8.0

## 推奨環境セットアップ方法

1. anacondaのインストール

https://www.anaconda.com/download/

2. 必要なライブラリのインストール

```terminal
$ pip install pyglet pymunk vispy keras tensorflow
```

## 実行方法

各章のフォルダへ移動してから実行してください。

```terminal
$ cd chap02
$ python game_of_life.py
```

詳しい実行方法は本書をご覧ください。

## その他注意点

### 6,7章で利用するkerasのバックエンドについて

kerasがインストール済みで、バックエンドをtensorflow以外に設定している場合はエラーが出るので、tensorflowに切り替えてください。

詳しくは
https://keras.io/ja/backend/

## ライセンス

本リポジトリのソースコードは[MITライセンス](http://www.opensource.org/licenses/MIT)です。
商用・非商用問わず、自由にご利用ください。
