from asyncio.windows_events import NULL
from email import contentmanager
import json

project_file = "./projects.json"
contributor_file = "./contributors.json"

with open(project_file,'r') as load_f:
    projects = json.load(load_f)
    print(projects)

with open(contributor_file,'r') as load_f:
    contributors = json.load(load_f)
    print(contributors)

def get_key( dict, value):
    print('value is ',value)
    for k,v in dict.items():
        print(v)
        try:
            if( v[value[0]] >= value[1]):
                print(dict[k])
                return k
        except:
            continue
    return []

solution = {}
contributor_busy = []
for project in projects:
    candidate_contributors = []
    print('project name ', project)
    project_dic = projects[project]
    skills = projects[project]['skills']
    print('skill needed ', skills)
    for skill in skills:
        skill_leve = skills[skill]
        print('skill level ', skill_leve[0])
        temp = [skill, int(skill_leve[0])]
        contributor = get_key(contributors, temp)
        if(contributor == []):
            print('not exist')
            break
        else:
            print('contributor is ', contributor)
        candidate_contributors.append(contributor)
    solution[project] = candidate_contributors

print('solution is ', solution )
submission_file = './b.txt'
f1 = open(submission_file,'w')

for v in solution:
    flag = 0
    if (  (NULL not in solution[v]) and ( '[]' not in solution[v]) ):
        
        print(type(solution[v]))
        print(v)
        if( solution[v]):
            f1.write(v)
            f1.write('\n')
        for t in solution[v]:
                flag += 1
                print(solution[v])
                #print(t)
                f1.write(t)
                f1.write(' ')
        if(flag > 0):
            f1.write('\n')
        
f1.close()


