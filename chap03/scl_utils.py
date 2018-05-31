import numpy as np

"""
４つのノイマン近傍の座標をリスト形式で返す
"""
def get_neumann_neighborhood(x, y, space_size):
    n = [((x+1)%space_size, y), ((x-1)%space_size, y), (x, (y+1)%space_size), (x, (y-1)%space_size)]
    return n

"""
ノイマン近傍の内、ランダムに１つの座標を返す
"""
def get_random_neumann_neighborhood(x, y, space_size):
    neighborhood = get_neumann_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

"""
8つのムーア近傍の座標をリスト形式で返す
"""
def get_moore_neighborhood(x, y, space_size):
    n = [((x-1)%space_size, (y-1)%space_size), (x, (y-1)%space_size), ((x+1)%space_size, (y-1)%space_size), \
         ((x-1)%space_size,  y              ),                        ((x+1)%space_size,  y              ), \
         ((x-1)%space_size, (y+1)%space_size), (x, (y+1)%space_size), ((x+1)%space_size, (y+1)%space_size)]
    return n

"""
ムーア近傍の内、ランダムに１つの座標を返す
"""
def get_random_moore_neighborhood(x, y, space_size):
    neighborhood = get_moore_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

"""
ムーア近傍の内、ランダムに2つの座標を返す
ただし２点は隣接していることを保証する
"""
def get_random_2_moore_neighborhood(x, y, space_size):
    n0_x, n0_y = get_random_moore_neighborhood(x, y, space_size)
    if x == n0_x:
        n1_x = np.random.choice([(n0_x+1)%space_size, (n0_x-1)%space_size])
        n1_y = n0_y
    elif y == n0_y:
        n1_x = n0_y
        n1_y = np.random.choice([(n0_y+1)%space_size, (n0_y-1)%space_size])
    else:
        n= [(x, n0_y), (n0_x, y)]
        n1_x, n1_y = n[np.random.randint(len(n))]
    return n0_x, n0_y, n1_x, n1_y

"""
(x, y)のムーア近傍の内、(n_x, n_y)に隣接する２つの座標を返す
(n_x, n_y)は必ず(x, y)のムーア近傍の座標を与えなければならない
"""
def get_adjacent_moore_neighborhood(x, y, n_x, n_y, space_size):
    if x == n_x:
        n0_x = (n_x-1)%space_size
        n0_y = n_y
        n1_x = (n_x+1)%space_size
        n1_y = n_y
    elif y == n_y:
        n0_x = n_x
        n0_y = (n_y-1)%space_size
        n1_x = n_x
        n1_y = (n_y+1)%space_size
    else:
        n0_x = x
        n0_y = n_y
        n1_x = n_x
        n1_y = y
    return n0_x, n0_y, n1_x, n1_y

"""
確率probabilityに従ってTrueかFalseを返す
probabilityは0から1の間を与えなければならない
"""
def evaluate_probability(probability):
    return np.random.rand() < probability
