# Chapter7 相互作用

## 実行方法

```terminal
$ python [gene file 1] [number of agents] [gene file 2] [number of agents] ...
```

複数のgene fileを指定し、それぞれの数を指定すると、集団でのシミュレーションを行う
gene fileは、chapter6で進化させたものを使う

例
99世代と89世代を10匹づつ
```terminal
$ python ant_nn_multi.py ../chap06_evolution/sampledata/gen0099_best.npy 10 ../chap06_evolution/sampledata/gen0089_best.npy 10
```
