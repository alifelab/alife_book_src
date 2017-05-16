# Gray-Scott model

## ソースコード解説 (gray_scott.py)

必要な前提知識

https://github.com/alifelab/alife_book_src/wiki

必要なライブラリとおまじない
```python
#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
```

シミュレーションを行う空間のサイズと各種パラメタを設定します。
X_SIZEは縦の大きさ, Y_SIZEは横の大きさです。
dxは空間の微分幅で、これが大きいと、「大きな空間を荒くシミュレーションする」。小さいと「小さな空間を細かくシミュレーションする」。設定になります。
とりあえず0.01で進めます。
dtは時間微分の幅です。こちらもとりあえず1で進めます。
visualization_stepはアニメーションを何ステップ毎に描画するか。
```python
# Simulation Parameters
X_SIZE = 256
Y_SIZE = 256
dx = 0.01
dt = 1
visualization_step = 16
```

モデルのパラメタです。
f, kを変えるとさまざまな振る舞いがみれます。
```python
Du = 2e-5
Dv = 1e-5
# amorphous
# f, k = 0.04, 0.06
# spots
# f, k = 0.035, 0.065
# wandering bubbles
# f, k = 0.012, 0.05
# waves
f, k = 0.025, 0.05
```

u,vの空間の中央に初期パターンを配置する。
初期パターンは20x20の正方形内はu=0.5, v=0.25になる。
```python
square_size = 20
u[X_SIZE//2-square_size//2:X_SIZE//2+square_size//2, Y_SIZE//2-square_size//2:Y_SIZE//2+square_size//2] = 0.5
v[X_SIZE//2-square_size//2:X_SIZE//2+square_size//2, Y_SIZE//2-square_size//2:Y_SIZE//2+square_size//2] = 0.25
```
ノイズを加えて、対象性を崩す
```python
u = u + u*np.random.rand(X_SIZE, Y_SIZE)*0.01
v = v + u*np.random.rand(X_SIZE, Y_SIZE)*0.01
```

ここでは、for文を使ってgridをそれぞれ計算するのではなく、行列演算で空間をまとめて計算している。
```python
# calculate laplacian
laplacian_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) + np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4*u) / (dx*dx)
laplacian_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) + np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4*v) / (dx*dx)
# Gray-Scott model equation
dudt = Du*laplacian_u - u*v*v + f*(1.0-u)
dvdt = Dv*laplacian_v + u*v*v - (f+k)*v
u += dt * dudt
v += dt * dvdt
```

## パラメタ空間版のラプラシアン計算解説

```python
        u_pad = np.pad(u, 1, 'edge')
        v_pad = np.pad(v, 1, 'edge')
        laplacian_u = (np.roll(u_pad, 1, axis=0) + np.roll(u_pad, -1, axis=0) + np.roll(u_pad, 1, axis=1) + np.roll(u_pad, -1, axis=1) - 4*u_pad) / (dx*dx)
        laplacian_v = (np.roll(v_pad, 1, axis=0) + np.roll(v_pad, -1, axis=0) + np.roll(v_pad, 1, axis=1) + np.roll(v_pad, -1, axis=1) - 4*v_pad) / (dx*dx)
        # next, remove edge value that extended before.
        laplacian_u = laplacian_u[1:-1,1:-1]
        laplacian_v = laplacian_v[1:-1,1:-1]
```
まず、u, vはX_SIZE x Y_SIZEの行列です。
これをそのままnp.roll()を用いて上下左右のセルをとってきてラプラシアンを計算すると、境界では反対側の値が使われます。(=周期境界）

そうすると、パラメタのk,fが非連続となってしまうのでこれを消したいです。

u_pad, v_padはu, vを上下左右に1サイズ拡張した行列です。（X_SIZE+2 x Y_SIZE+2）

新しい境界はもともとの境界の値で埋められます

np.pad()の説明
https://github.com/alifelab/alife_book_src/wiki#%E8%A1%8C%E5%88%97%E3%81%AE%E3%82%B7%E3%83%95%E3%83%88%EF%BC%92

これを用いてラプラシアンを計算すると、境界は常にその内部の値と同じ値を取るという条件になります. （=境界外からの拡散がゼロ）

その後、laplacian_u[1:-1,1:-1]で、最初と最後の要素（=上で追加した境界部分）を消して、元のサイズに戻します.




## References

John E. Pearson (1993) "Complex Patterns in a Simple System" Science 261(5118):189-192.

http://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/
