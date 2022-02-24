#!/usr/bin/env python3

import argparse
import json
import copy
import random
import time

parser = argparse.ArgumentParser(description='Hash 2022 Practice')

parser.add_argument(
    '--input', type=str, required=True,
    help='the input file'
)


args = parser.parse_args()


with open(args.input, 'r') as f:
    lines = f.readlines()

contributor_count, project_count = int(lines[0].split(" "))
print("{} contributors, {} projects".format(contributor_count, project_count))

# for i in range(1, len(lines)):
#     line = lines[i]


#     people_id = int((i+1) / 2)
#     people_key = "people" + str(people_id)
#     if people_key not in people_dict:
#         people_dict[people_key] = {
#             "like": {},
#             "dislike": {}
#         }
#     taste_key = "like"
#     if i % 2 == 0:
#         taste_key = "dislike"
#     xc = 0
#     for x in line.split(" "):
#         xc += 1
#         if xc ==1:
#             continue
#         if "\n" in x:
#             x = x[:-1]
#         people_dict[people_key][taste_key][x] = True
#         if x not in gredient_dict:
#             gredient_dict[x] = {
#                 "like": {},
#                 "dislike": {}
#             }
#         gredient_dict[x][taste_key][people_key] = True