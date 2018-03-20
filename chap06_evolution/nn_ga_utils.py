def get_gene_length(model):
    return len(encode_weights(model))


def encode_weights(model):
    w = model.get_weights()
    g = np.concatenate([x.flatten() for x in w])
    return g


def decode_weights(model, gen):
    w_shape = [wi.shape for wi in model.get_weights()]
    w_size = [wi.size for wi in model.get_weights()]

    w = []
    tmp = gen
    for shape, size in zip(w_shape, w_size):
        w.append(tmp[:size].reshape(shape))
        tmp = tmp[size:]
    model.set_weights(w)
