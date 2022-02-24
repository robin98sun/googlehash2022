#!/usr/bin/env python3

import argparse
import json
import copy
import random
import time

project_file = "./projects.json"
contributor_file = "./contributors.json"


parser = argparse.ArgumentParser(description='Hash 2022 Practice')
parser.add_argument(
    '--output', type=str, required=False,
    help='the output file'
)
args = parser.parse_args()


with open(project_file, 'r') as f:
    projects = json.load(f)

with open(contributor_file, 'r') as f:
    contributors = json.load(f)


print("{} contributors in memory".format(len(contributors)))
print("{} projects in memory".format(len(projects)))

contributor_list = []

project_queue = []
max_timestamp = 0
for proj_name in projects:
    proj_obj = projects[proj_name]
    proj_obj["name"] = proj_name
    project_queue.append(proj_obj)
    if proj_obj["deadline"] + proj_obj["days"] > max_timestamp:
        max_timestamp = proj_obj["deadline"] + proj_obj["days"]
    # elif proj_obj["deadline"] + proj_obj["score"] > max_timestamp:
    #     max_timestamp = proj_obj["deadline"] + proj_obj["score"]

for contr_name in contributors:
    contr_obj = contributors[contr_name]
    contr_obj["_name_"] = contr_name
    contributor_list.append(contr_obj)

contributor_list.sort(key = lambda c: len(c))

def shuffle_contributors():
    contributor_list.sort(key = lambda c: random.random())    

def check_contributor_available(contributor_name):
    if contributor_name not in contributors:
        return False
    if "_working_" not in contributors[contributor_name]:
        contributors[contributor_name]["_working_"] = None
        return True
    elif contributors[contributor_name]["_working_"] is None:
        return False
    return False

def assign_contributor(contributor_name, project_name, timestamp):
    if "assigned-projects" not in contributors[contributor_name]:
        contributors[contributor_name]["assigned-projects"] = []
    if check_contributor_available(contributor_name):
        contributors[contributor_name]["assigned-projects"].append({
            "project": project_name,
            "start": timestamp,
            "end": None,
        })
        contributors[contributor_name]["_working_"] = project_name

def release_contributor(contributor_name, project_name, timestamp):    
    contributors[contributor_name]["_working_"] = None
    for proj in contributors[contributor_name]["assigned-projects"]:
        if proj["project"] == project_name:
            proj["end"] = timestamp
            break

def find_available_contributor(skill, level, no_in_filter):
    for contr_obj in contributor_list:
        contr_name = contr_obj["_name_"]
        if contr_name in no_in_filter:
            continue

        if "_working_" in contr_obj and contr_obj["_working_"] is not None:
            continue

        skill_set = copy.deepcopy(contr_obj)
        if skill in skill_set:
            if skill_set[skill] > level:
                return 3, skill_set
            elif skill_set[skill] == level:
                return 2, skill_set
            elif skill_set[skill] == level - 1:
                return 1, skill_set
        elif level == 1:
            return 1, skill_set

    return 0, None

def schedule_projects(mechanism, queue, max_timestamp):
    if mechanism == "ddl":
        queue.sort(key = lambda proj: proj["deadline"] - proj["days"])



    timestamp = 0
    working_projects = {}
    finished_projects = {}
    project_sequence = []

    shuffle_limit = 10

    print("scheduling in [{}] mechanism".format(mechanism))
    while timestamp < max_timestamp:
        print("  current time: {}, max time: {}, working projects: {}, finished projects: {}".format(
            timestamp, max_timestamp, len(working_projects), len(finished_projects),
        ))
        for proj in queue:
            if proj["name"] in working_projects:
                continue
            if proj["name"] in finished_projects:
                continue

            shuffle_idx = 0

            available_contributors = {}
            is_project_workable = True

            while shuffle_idx < shuffle_limit:
                for skill_name in proj["skills-in-order"]:
                    recruitments =  copy.deepcopy(proj["skills"][skill_name])
                    recruitments.sort(reverse=True)
                    has_leader = False
                    is_skill_fulfill = True
                    assigned_indexes = {}
                    for level in recruitments:
                        available_level, contr_obj = find_available_contributor(skill_name, level, available_contributors)
                        is_contr_usable = False

                        if available_level > 1:
                            has_leader = True
                            is_contr_usable = True
                        elif available_level == 1:
                            if not has_leader:
                                for ac_key in available_contributors:
                                    ac = available_contributors[ac_key]
                                    if skill_name in ac and ac[skill_name] >= level:
                                        has_leader = True
                                        break
                            if has_leader:
                                is_contr_usable = True
                            else:
                                is_skill_fulfill = False
                        else:
                            is_skill_fulfill = False
                        if not is_skill_fulfill:
                            is_project_workable = False
                            break
                        if is_contr_usable and contr_obj is not None:
                            index_in_position_desc = 0
                            for i in range(len(proj["skills"][skill_name])):
                                if proj["skills"][skill_name][i] == level:
                                    idx_key = "idx" + str(i)
                                    if idx_key not in assigned_indexes:
                                        assigned_indexes[idx_key] = contr_obj
                                        index_in_position_desc = i
                                        break
                            available_contributors[contr_obj["_name_"]] = {
                                "skill": skill_name,
                                "index-in-desc": index_in_position_desc,
                                "contributor": contr_obj,
                            }

                    if not is_project_workable:
                        break

                if is_project_workable:
                    if timestamp + proj["days"] >= proj["deadline"] + proj["score"]:
                        is_project_workable = False

                if is_project_workable:
                    for contr_name in available_contributors:
                        assign_contributor(contr_name, proj["name"], timestamp)
                    working_projects[proj["name"]] = proj
                    proj["start"] = timestamp
                    proj["assigned-contributors"] = available_contributors
                    project_sequence.append(proj)
                    break
                else:
                    shuffle_idx += 1
                    shuffle_contributors()


        finished_at_this_time = []
        for proj_name in working_projects:
            proj = working_projects[proj_name]
            if timestamp - proj["start"] >= proj["days"]:
                finished_projects[proj_name] = proj
                proj["end"] = timestamp
                for contr_name in proj["assigned-contributors"]:
                    release_contributor(contr_name, proj_name, timestamp)
                finished_at_this_time.append(proj)

        for p in finished_at_this_time:
            del working_projects[p["name"]]

        if len(finished_at_this_time):
            lines = []
            line = str(len(finished_projects)) + "\n"
            lines.append(line)
            for proj in project_sequence:
                if "end" in proj and proj["end"] is not None:
                    lines.append(proj["name"]+"\n")
                    for skill in proj["skills-in-order"]:
                        for idx in range(len(proj["skills"][skill])):
                            for contr_name in proj["assigned-contributors"]:
                                contr = proj["assigned-contributors"][contr_name]
                                if contr["skill"] == skill and idx == contr["index-in-desc"]:
                                    lines.append(contr["contributor"]["_name_"]+"\n")
            with open(args.output, "w") as f:
                f.writelines(lines)


        timestamp += 1


    with open("./queue.json", "w") as f:
        json.dump(queue, f, indent=4)

    with open("./sequence.json", "w") as f:
        json.dump(project_sequence, f, indent=4)

schedule_projects("ddl", project_queue, max_timestamp)








