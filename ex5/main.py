import requests
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from arabic_reshaper import reshape

# start_urls = [
#     'https://ganj.irandoc.ac.ir/api/v1/search/main?basicscope=5&fulltext_status=1&keywords=مجید+شیخ%E2%80%8Cمحمدی&limitation=&results_per_page=4&sort_by=1&year_from=0&year_to=1400'
# ]

# filename = 'article-ids.txt'

# with open(filename, 'a+') as f:
#     for url in start_urls:
#         res = requests.get(url)
#         res = res.json()
#         for element in res['results']:
#             f.write(element['uuid'] + "\n")
#     print('Saved!')

with open('article-ids.txt', 'r') as f:
    ids = f.readlines()
    urls = []
    for id in ids:
        urls.append(
            f'https://ganj.irandoc.ac.ir/api/v1/articles/{id.strip()}/show_tags')
    global_tags = {}
    for url in urls:
        res = requests.get(url)
        res = res.json()
        article_id = url.split("/")[-2]
        tag_file_name = f'tags-{article_id}.txt'
        with open(tag_file_name, 'a') as f:
            for element in res['tags']:
                if(element['title_fa'] in global_tags):
                    global_tags[element['title_fa']] += 1
                else:
                    global_tags[element['title_fa']] = 1
                f.write(element['title_fa'] + "\n")
    np.save('visualize.npy', global_tags)


# read_dictionary = np.load('visualize.npy', allow_pickle='TRUE').item()
# new_dict = {}

# for key, value in read_dictionary.items():
#     if(value > 2):
#         new_dict[key] = value

# sorted_dict = {}
# sorted_keys = sorted(new_dict, key=new_dict.get)  # [1, 3, 2]

# for w in sorted_keys:
#     sorted_dict[w] = new_dict[w]

# persian_labels = [get_display(reshape(label))
#                   for label in list(sorted_dict.keys())]


# plt.bar(persian_labels, sorted_dict.values(), color='g')
# plt.xticks(rotation=90)
# plt.show()
