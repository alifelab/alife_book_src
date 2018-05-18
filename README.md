# alife_book_src

## development environment

**anaconda3-5.0.0 is recommended.**

- python 3.5.1
- numpy 1.12.1
- matplotlib 2.0.0


## セットアップ

1. anacondaのインストール

https://www.anaconda.com/download/

2. 必要なライブラリのインストール

```terminal
$ pip install pyglet pymunk vispy keras pygame Pillow
```

### kerasのバックエンドについて
kerasがインストール済みで、バックエンドをtensorflow以外に設定している場合はエラーが出るので、tensorflowに切り替えてください.
https://keras.io/ja/backend/
