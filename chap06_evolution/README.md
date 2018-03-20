# Chapter6 進化

## 実行方法

### GA

```terminal
$ python ant_nn_ga.py
```

ターミナルに世代ごとのfitnessの平均・標準偏差・最大・最小が表示される.

実行したディレクトリには、各世代の最大fitnessの個体のgene (NNのweight)が保存される.


### 1 agent simulation

```terminal
$ python ant_nn.py [gene file]
```

\[gene file\]には, GAで生成されたファイルか、sampledataディレクトリ内のものを利用.
