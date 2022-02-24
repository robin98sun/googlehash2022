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

parser.add_argument(
    '--rounds', type=int, required=False, default=10,
    help='rounds to go through'
)

args = parser.parse_args()


with open(args.input, 'r') as f:
    lines = f.readlines()

people_count = int(lines[0])

print("{} people".format(people_count))

gredient_dict = {}
people_dict = {}

for i in range(1, len(lines)):
    line = lines[i]
    people_id = int((i+1) / 2)
    people_key = "people" + str(people_id)
    if people_key not in people_dict:
        people_dict[people_key] = {
            "like": {},
            "dislike": {}
        }
    taste_key = "like"
    if i % 2 == 0:
        taste_key = "dislike"
    xc = 0
    for x in line.split(" "):
        xc += 1
        if xc ==1:
            continue
        if "\n" in x:
            x = x[:-1]
        people_dict[people_key][taste_key][x] = True
        if x not in gredient_dict:
            gredient_dict[x] = {
                "like": {},
                "dislike": {}
            }
        gredient_dict[x][taste_key][people_key] = True

print("{} gredient".format(len(gredient_dict.keys())))

gredient_list = []
for g in gredient_dict:
    gredient_list.append({
            "name": g,
            "like": len(gredient_dict[g]["like"].keys()),
            "dislike": len(gredient_dict[g]["dislike"].keys()),
        })

gredient_list.sort(key = lambda x: x["dislike"])
gredient_list.sort(key = lambda x: len(people_dict) - x["like"])
with open(args.input + ".gredient.stat.asc.json", 'w') as f:
    json.dump(gredient_list, f, indent=4)

with open(args.input + ".people.stat.json", 'w') as f:
    json.dump(people_dict, f, indent=4)


selected = {}
for g in gredient_list:
    if g["like"] > g["dislike"]:
        selected[g["name"]] = True

print("{} selected gredients".format(len(selected)))

def count_satisfied_people(selected_gredients):

    satisfied_count = 0
    for people_key in people_dict:
        satisfied = True
        people = people_dict[people_key]
        for g in people["dislike"]:
            if g in selected_gredients:
                satisfied = False
                break
        for g in people["like"]:
            if g not in selected_gredients:
                satisfied = False
                break
        if satisfied:
            satisfied_count += 1

    return satisfied_count

print("{} satisfied people".format(count_satisfied_people(selected)))


print("...")
print("one by one")
def select_gredients_one_by_one(sorted_gredient_list, selected_gredients={}, is_to_append=True):
    satisfied_count = count_satisfied_people(selected_gredients)
    try_to_select = copy.deepcopy(selected_gredients)
    selected = copy.deepcopy(selected_gredients)
    i = 0
    for g in gredient_list:
        i+=1
        gredient_name = g["name"]
        need_to_count = False
        if is_to_append:
            if gredient_name not in try_to_select:
                try_to_select[gredient_name] = True
                need_to_count = True
        elif gredient_name in try_to_select:
            del(try_to_select[gredient_name])
            need_to_count = True

        if not need_to_count:
            continue

        people_count_try_to_satisfy = count_satisfied_people(try_to_select)
        
        if people_count_try_to_satisfy >= satisfied_count:
        # if (people_count_try_to_satisfy >= satisfied_count and is_to_append) \
            # or (people_count_try_to_satisfy > satisfied_count and not is_to_append):
            satisfied_count = people_count_try_to_satisfy
            if is_to_append:
                selected[gredient_name] = True
            elif gredient_name in selected:
                del(selected[gredient_name])
        else:
            if is_to_append:
                del(try_to_select[gredient_name])
            else:
                try_to_select[gredient_name] = True

        # print("     [{}: {}] {} selected gredient, {} satisfied people".format(i,gredient_name, len(selected), satisfied_count))
    print("{} selected gredient, {} satisfied people".format( len(selected), satisfied_count) )
    return selected

def dual_direction_selection(selected = {}):
    first_selected = select_gredients_one_by_one(gredient_list, selected)
    gredient_list.sort(key = lambda x: random.random())
    # gredient_list.sort(key = lambda x: - x["dislike"])
    # gredient_list.sort(key = lambda x: x["like"])
    with open(args.input + ".gredient.stat.dsc.json", 'w') as f:
        json.dump(gredient_list, f, indent=4)
    final_selected = select_gredients_one_by_one(gredient_list, first_selected, is_to_append = False)

    return final_selected

final_selected = {}
random.seed(time.time())
for r in range(args.rounds):
    final_selected = dual_direction_selection(final_selected)
    print("round [{}] is done".format(r))

with open(args.input + '.output.txt', 'w') as f:
    line = str(len(final_selected))
    for g in final_selected:
        line += " " + g

    f.writelines([line])






