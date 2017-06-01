# SCL model

## プログラム解説

Particleの種類は以下

S: Substrate
K: Catalyst
L: Link
H: Hole

### プロシージャ概要

全てのx,yに関して, 座標(x,y)にあるparticle(primary particle)に関して

1. Movement
2. Reaction
2.2 production
2.3 disintegration
2.4 bonding
2.5 bond_decay
2.6 absorption
2.7 emission

を順に実行していく.

各reactionは, まずneighborhood particleをランダムに選び、特定の条件をクリアした場合のみある確率で当該のreactionが行われるという流れ.

### Production
最初に**隣接する**２つのneighborhood particleを選択する.

条件
- primary particleがKである
- neighborhood particleが両方共Sである

これらの条件を満たした場合、ある確率で
- neighborhood particle 0をHに
- neighborhood particle 1をLに
に変更する

### disintegration
編集中

### bonding
編集中

### bond_decay
編集中

### absorption
編集中

### emission
編集中

## References
編集中

McMullin, Barry. "SCL: An artificial chemistry in Swarm." Santa Fe, NM 87501, USA: Santa Fe Institute, 1997.
https://www.santafe.edu/research/results/working-papers/scl-an-artificial-chemistry-in-swarm

## プログラミング参考ページ

https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html

https://matplotlib.org/examples/specialty_plots/hinton_demo.html
