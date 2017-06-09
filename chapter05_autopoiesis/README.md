# SCL model

## プログラム解説

Particleの種類は以下

S: Substrate
K: Catalyst
L: Link
H: Hole
LS: Link + Substrate

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
1. **隣接する**２つのneighborhood particleを選択する.
2. 以下の条件をチェックする
- primary particleがKである
- neighborhood particleが両方共Sである
3. 確率*PRODUCTION_PROBABILITY*で以下の遷移を行う
- neighborhood particle 0 => H
- neighborhood particle 1 => L

### disintegration
編集中

### bonding
編集中

### bond_decay
編集中

### absorption

LinkがSubstrateを吸収する反応.
これは、emissionと合わせて、linkがsubstrateを透過する振る舞いを実現している.

1. 1つのneighborhood particleを選択する
2. 以下の条件をチェック
- primary particleがLである
- neighborhood particleがSである
3. 確率*ABSORPTION_PROBABILITY*で以下の遷移
primary particle => LS
neighborhood particle => H

### emission

LinkがSubstrateを放射する反応.
これは、absorptionと合わせて、linkがsubstrateを透過する振る舞いを実現している.

1. 1つのneighborhood particleを選択する
2. 以下の条件をチェック
- primary particleがLSである
- neighborhood particleがHである
3. 確率*EMISSION_PROBABILITY*で以下の遷移
primary particle => L
neighborhood particle => S

## References
編集中

McMullin, Barry. "SCL: An artificial chemistry in Swarm." Santa Fe, NM 87501, USA: Santa Fe Institute, 1997.
https://www.santafe.edu/research/results/working-papers/scl-an-artificial-chemistry-in-swarm

## プログラミング参考ページ

https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html

https://matplotlib.org/examples/specialty_plots/hinton_demo.html
