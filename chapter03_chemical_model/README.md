# Gray-Scott model

## 解説

### 必要な関数知識

#### 行列の生成
```python
np.ones((x,y))
np.zeros((x,y))
```
全て1/0で埋めたx行y列の行列を生成する。

#### 行列のシフト
```python
np.roll(x, n, axis)
```
行列xをaxis方向にn個ずらす。
例えば
```python
x = np.array([[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]])
```
とすると、
```
np.roll(x, 1, axis=0)
np.roll(x, 1, axis=1)
```
はそれぞれ
```python
array([[6, 7, 8],
       [0, 1, 2],
       [3, 4, 5]])
array([[2, 0, 1],
       [5, 3, 4],
       [8, 6, 7]])
```
となる。



### ソースコード解説 (gray_scott.py)

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

## References

John E. Pearson (1993) "Complex Patterns in a Simple System" Science 261(5118):189-192.

http://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/
