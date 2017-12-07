## アーノルドのネコ写像

https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%BC%E3%83%8E%E3%83%AB%E3%83%89%E3%81%AE%E7%8C%AB%E5%86%99%E5%83%8F

### 使い方

```sh
$ python cat_map.py sample.png
```

### ソースコード解説

画像データの読み込み
```python
img_array = imread(sys.argv[1])
```

x, yは画像と同じ形状の2次元配列で、各ピクセルのx座標、y座標
https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.meshgrid.html
```python
x, y = np.meshgrid(range(x_size), range(y_size))
```

x, yからx_map, y_mapを作成する
x_map, y_mapには、変換後の画像が参照するべき元のx, y座標が入る
```python
x_map = (2*x + y) % x_size
y_map = (x + y) % y_size
```

変換
```python
img_array = img_array[y_map, x_map]
```
