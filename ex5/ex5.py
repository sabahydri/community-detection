import igraph as ig
import numpy as np
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


read_dictionary = np.load('visualize.npy', allow_pickle='TRUE').item()

tag_to_number_map = {}
i = 0
for key, value in read_dictionary.items():
    if(value > 1):
        tag_to_number_map[key.strip()] = i
        i += 1

filename = 'article-ids.txt'
ids = []
tags2D = []
flat_tags = []
with open(filename, 'r') as f:
    ids = f.readlines()
    
for id in ids:
    filename = f'tags-{id.strip()}.txt'
    with open(filename, 'r') as f:
        all_tags = f.readlines()
        all_tags = list(map(str.strip, all_tags))
        valid_tags = [value for value in all_tags if value in tag_to_number_map.keys()]
        tags2D.append(list(map(str.strip, valid_tags)))

flat_tags = [item for sublist in tags2D for item in sublist]

    
matrix = csr_matrix((len(flat_tags), len(ids)), dtype=np.int8).toarray()
for i in range(len(flat_tags)):
    for j in range(len(ids)):
        if(flat_tags[i] in tags2D[j]):
            matrix[i][j] += 1

adj = np.matmul(matrix, matrix.T)
    
g = ig.Graph.Weighted_Adjacency(adj, mode="undirected", loops=False)

weights = [item for sublist in adj for item in sublist]

g.es["label"] = weights
g.es["weight"] = weights

g.es.select(weight=0).delete()
g.vs.select(_degree = 0).delete()

g_deg = g.degree()
g_deg = list(map(lambda num:num*10, g_deg))


print(tag_to_number_map)
layout = g.layout('kk')
visual_style = {}
visual_style["vertex_size"]= g_deg
visual_style["vertex_color"] = ['pink' for v in g.vs]
visual_style["vertex_label"] = [get_display(reshape(tag))
                for tag in list(tag_to_number_map.keys())]
ig.plot(g, **visual_style, bbox = (1000,1000), target='myfile.svg')



multilevel_community = g.community_multilevel()
visual_style = {}
visual_style["vertex_size"]= g_deg
visual_style["vertex_label"] = [get_display(reshape(tag))
                for tag in list(tag_to_number_map.keys())]
ig.plot(multilevel_community, **visual_style, bbox = (1000,1000),target='myfile2.svg')


propagation_community = g.community_label_propagation()



visual_style = {}
visual_style["vertex_size"]= g_deg
visual_style["vertex_label"] = [get_display(reshape(tag))
                for tag in list(tag_to_number_map.keys())]
ig.plot(propagation_community, **visual_style, bbox = (1000,1000),target='myfile3.svg')


leading_community=g.community_leading_eigenvector()
visual_style = {}
visual_style["vertex_size"]= g_deg
visual_style["vertex_label"] = [get_display(reshape(tag))
                for tag in list(tag_to_number_map.keys())]
ig.plot(leading_community, **visual_style, bbox = (1000,1000),target='myfile4.svg')


print(ig.compare_communities(multilevel_community, propagation_community, method='vi', remove_none=False))
print(ig.compare_communities(leading_community, propagation_community, method='vi', remove_none=False))

print(g.modularity(multilevel_community, weights=None))
print(g.modularity(propagation_community, weights=None))
print(g.modularity(leading_community, weights=None))























