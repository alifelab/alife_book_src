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


## System Description

### Neural Network

#### Overview

- Input: 7 (sensor) + 2 (context neuron)
- Hidden: 4
sigmoid activation
- Output: 2 (speed + rotation) + 2 (context neuron)
sigmoid activation

#### Code

```python
CONTEXT_NN_NUM = 2

nn_model = Sequential()
nn_model.add(InputLayer((7+CONTEXT_NN_NUM,)))
nn_model.add(Dense(4, activation='sigmoid'))
nn_model.add(Dense(2+CONTEXT_NN_NUM, activation='sigmoid'))
context_val = np.zeros(CONTEXT_NN_NUM)
```

Sequential()
系列モデル
単純な層の重ね合わせ

InputLayer()
入力レイヤー

Dense()
全結合レイヤー
context neuronの出力を保存しておく変数
次のステップでセンサー入力と共にinputに入れる


### 遺伝的アルゴリズム

#### Overview

1. evaluation and selection
- エサの総取得数をfittnessとして、トーナメント選択でPARENT_NUMだけparentsを選択する
- best fittness agentをoffspringに加える
- parentsからランダムに選択してoffspringに加える
- 上記をPOPULATION_SIZE/3-1回繰り返す

2. mutation
- parentsからランダムに選択したagentのgeneの１箇所に正規分布ノイズを加えて、offsprintに加える.
- 上記をPOPULATION_SIZE/3回繰り返す


3. crossover
- parentsからランダムに2つ選択する
- ランダムなcross over pointで２つのgeneを配合して、offspringに加える
- 上記をPOPULATION_SIZE/3回繰り返す

4. offspringsを次のpopulationとする


#### Code

```python
# GA and trial parameters
ONE_TRIAL_STEP = 5000
POPULATION_SIZE = 50
TORNAMENT_SIZE = 5

.........

    # evaluate population
    for g in population:
        print('.', end='', flush=True)
        # decode gene and set weights on NN
        decode_weights(nn_model, g)

        # start trial
        obs = sim.reset()
        for i in range(ONE_TRIAL_STEP):
            act = action(obs)
            obs = sim.step(act)

        # get fitness of this trial
        fitness.append(sim.get_fitness()[0])

.........

    np.random.seed()

    # selection
    TORNAMENT_SIZE = 5
    PARENT_NUM = POPULATION_SIZE // 2
    parents = []
    for i in range(PARENT_NUM):
        idxs = np.random.randint(0, len(population), TORNAMENT_SIZE)
        fits = np.array(fitness)[idxs]
        winner_idx = idxs[np.argmax(fits)]
        parents.append(population[winner_idx])

    # best population alive next gen
    population[0] = best_pop

    # same as parents N/3
    for i in range(1, POPULATION_SIZE//3):
        offspring_idx = np.random.randint(0, PARENT_NUM)
        offspring = parents[offspring_idx]
        population[i] = offspring


    # mutation N/3
    for i in range(POPULATION_SIZE//3, 2*POPULATION_SIZE//3):
        offspring_idx = np.random.randint(0, PARENT_NUM)
        offspring = parents[offspring_idx]
        mut_idx = np.random.randint(0, gene_length)
        offspring[mut_idx] += np.random.randn()
        population[i] = offspring


    # crossover N/3
    for i in range(2*POPULATION_SIZE//3, POPULATION_SIZE):
        idx1 = np.random.randint(0, PARENT_NUM)
        p1 = parents[idx1]
        idx2 = np.random.randint(0, PARENT_NUM)
        p2 = parents[idx2]
        xo_idx = np.random.randint(1, gene_length)
        offspring = np.r_[p1[:xo_idx], p2[xo_idx:]]
        population[i] = offspring
```
