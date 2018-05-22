from scl_utils import *

def production(particles, x, y, probability):
    p = particles[x,y]
    n0_x, n0_y, n1_x, n1_y = get_random_2_moore_neighborhood(x, y, particles.shape[0])
    n0_p = particles[n0_x, n0_y]
    n1_p = particles[n1_x, n1_y]
    if p['type'] != 'CATALYST' or n0_p['type'] != 'SUBSTRATE' or n1_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        n0_p['type'] = 'HOLE'
        n1_p['type'] = 'LINK'


def disintegration(particles, x, y, probability):
    p = particles[x,y]
    # disintegrationはすぐに起こらない場合もあるので、一旦フラグを立てる
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
        p['disintegrating_frag'] = True

    if not p['disintegrating_frag']:
        return
    # LINKがSUBSTRATEを含む場合には、強制的に放出する
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK_SUBSTRATE' and n_p['type'] == 'HOLE':
        p['type']   = 'LINK'
        n_p['type'] = 'SUBSTRATE'
    # disintegration
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK' and n_p['type'] == 'HOLE':
        # disintegrationが起こる時は、LINKに繋がったbondは全て壊れる
        for b in p['bonds']:
            particles[b[0], b[1]]['bonds'].remove((x, y))
        p['bonds'] = []
        p['type']   = 'SUBSTRATE'
        n_p['type'] = 'SUBSTRATE'
        p['disintegrating_frag'] = False


def bonding(particles, x, y, chain_initiate_prob, chain_splice_prob, chain_extend_prob):
    p = particles[x,y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    if not n_p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    if (n_x, n_y) in p['bonds']:
        return
    if len(p['bonds']) >= 2 or len(n_p['bonds']) >= 2:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in p['bonds'] or (an1_x, an1_y) in p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(n_x, n_y, x, y, particles.shape[0])
    if (an0_x, an0_y) in n_p['bonds'] or (an1_x, an1_y) in n_p['bonds']:
        return

    # Bondingは以下の２つの場合には起こらない
    # 1) moore近傍にすでに結合している膜分子がある場合 (chainInhibitBond)
    # 2) moore近傍に触媒分子が存在する場合 (catInhibitBond)
    mn_list = get_moore_neighborhood(x, y, particles.shape[0])
    for x1, y1 in mn_list:
        # if particles[x1,y1]['type'] is 'CATALYST':
        #     return
        for x2, y2 in mn_list:
            if (x2, y2) in particles[x1,y1]['bonds']:
                return
    mn_list = get_moore_neighborhood(n_x, n_y, particles.shape[0])
    for x1, y1 in mn_list:
        # if particles[x1,y1]['type'] is 'CATALYST':
        #     return
        for x2, y2 in mn_list:
            if (x2, y2) in particles[x1,y1]['bonds']:
                return

    if len(p['bonds'])==0 and len(n_p['bonds'])==0:
        prob = chain_initiate_prob
    elif len(p['bonds'])==1 and len(n_p['bonds'])==1:
        prob = chain_splice_prob
    else:
        prob = chain_extend_prob
    if evaluate_probability(prob):
        p['bonds'].append((n_x, n_y))
        n_p['bonds'].append((x, y))


def bond_decay(particles, x, y, probability):
    p = particles[x,y]
    if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    for b in p['bonds']:
        if evaluate_probability(probability):
            pass


def absorption(particles, x, y, probability):
    p = particles[x,y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK' or n_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        p['type']   = 'LINK_SUBSTRATE'
        n_p['type'] = 'HOLE'


def emission(particles, x, y, probability):
    p = particles[x,y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK_SUBSTRATE' or n_p['type'] != 'HOLE':
        return
    if evaluate_probability(probability):
        p['type']   = 'LINK'
        n_p['type'] = 'SUBSTRATE'
