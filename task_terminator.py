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

contributor_count, project_count = lines[0][:-1].split(" ")
contributor_count, project_count = int(contributor_count), int(project_count)
print("{} contributors, {} projects".format(contributor_count, project_count))


contributors = {}
expertises = {}
projects = {}

contributor_pointer = 0
expertise_pointer = 0
project_pointer = 0
skill_pointer = 0

contributor_name, expertise_count = "", 0

project_name, days, scores, deadline, skill_requirements = "", 0, 0, 0, 0

reading_target="contributors"

for i in range(1, len(lines)):
    line = lines[i][:-1]
    if reading_target == "contributors":

        contributor_name, expertise_count = line.split(" ")
        expertise_count = int(expertise_count)

        if contributor_name not in contributors:
            contributors[contributor_name] = {}

        reading_target = "expertises"
        contributor_pointer += 1

    elif reading_target == "expertises":
        skill, level = line.split(" ")
        level = int(level)
        contributors[contributor_name][skill] = level
        expertise_pointer += 1
        if expertise_pointer >= expertise_count:
            if contributor_pointer >= contributor_count:
                reading_target = "project"
            else:
                reading_target = "contributors"
                expertise_pointer = 0

    elif reading_target == "project":
        project_name, days, scores, deadline, skill_requirements = line.split(" ")
        days, scores, deadline, skill_requirements = int(days), int(scores), int(deadline), int(skill_requirements)
        if project_name not in projects:
            projects[project_name] = {
                "score": scores,
                "days": days,
                "deadline": deadline,
                "skills": {}
            }

        project_pointer += 1
        reading_target = "skill-requirements"

    elif reading_target == "skill-requirements":
        skill_name, level = line.split(" ")
        level = int(level)
        projects[project_name]["skills"][skill_name] = level
        skill_pointer += 1
        if skill_pointer >= skill_requirements:
            if project_pointer >= project_count:
                break
            else:
                reading_target = "project"
                skill_pointer = 0

project_file = "./projects.json"
contributor_file = "./contributors.json"

print("{} contributors in memory".format(len(contributors)))
print("{} projects in memory".format(len(projects)))

with open(project_file, 'w') as f:
    json.dump(projects, f, indent=4)

with open(contributor_file, 'w') as f:
    json.dump(contributors, f, indent=4)








