import numpy as np
import lyricsgenius

path = './embeddings_24-11-26/'

id_embeddings = np.load(path + 'id_embeddings_330.npy')
embeddings = np.load(path + 'embeddings_330.npy')

print(id_embeddings)