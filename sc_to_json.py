import json
import os
import time
import math


def to_json(sourcefile, filename_target, systemname, nickname = None):
    if nickname is None:
        nickname = systemname
    mult_dic = {"IceWorld": 1.02, "Desert": 1.12, "Selena": 1.05, "IceGiant": 0.88, "Asteroid": 1, "Comet": 0.95, "Terra": 1.63,
                "Oceania": 1.20, "GasGiant": 0.80, "Titan": 1.10}
    earth_mass = 5.972e+24
    final_target = filename_target + '.json'
    with open(sourcefile) as source_file:
        k = source_file.readlines()
    k_2 = []
    all_file = [f for f in os.listdir('.') if os.path.isfile(f)]
    if filename_target in all_file:
        with open(final_target) as target:
            se_data = json.load(target)
    else:
        se_data = {}
    for values in k:
        if values != '\n':
            values = values.replace('"','')
            if len(values) - len(values.lstrip('\t')) == 0 and len(values.split()) > 1:
                body_name = values.split()
                body_class = body_name[0]
                body_name[0] = '"'
                body_name[1] = body_class + ' ' + body_name[1]
                body_name.append('" :')
                k_2.append(''.join(body_name))
            elif '{' in values or '}' in values:
                k_2.append(values)
            elif len(values.lstrip('\t')) != 0:
                body_data = values.split()
                if len(body_data) != 1:
                    body_data.insert(0,'"')
                    body_data.insert(2,'" :"')
                    body_data.append('",')
                    k_2.append(''.join(body_data))
                else:
                    k_2.append('"{0}":'.format(''.join(body_data)))

    #Fixing commas and stuff
    for lineno in range(len(k_2)):
        t = k_2[lineno]
        if '{' in t.split() or '}' in t.split():
            if k_2[lineno-1].endswith(','):
                k_2[lineno-1] = k_2[lineno-1].replace(',','')
            if '}' in t.split():
                k_2[lineno] = '},'
    k_2[-1] = '}'
    a = '{\n' + '\n'.join(k_2) + '\n}'
    js = json.loads(a)
    bodies = list(js.keys())
    op_js = {}
    op_js['body_count'] = {}
    op_js['body_count']['all'] = len(bodies)
    op_js['value'] = 1000
    op_js['body_names'] = {}
    for body in bodies:
        body_type = body.split()[0]
        just_name = body.split()[1]
        if body_type != "Barycenter":
            if 'Mass' in list(js[body].keys()) and js[body]['Class'] in list(mult_dic.keys()):
                indiv_value = math.log10(earth_mass*float(js[body]['Mass']))-10
                indiv_value = indiv_value*mult_dic[js[body]['Class']] 
                if indiv_value > 0:
                    op_js['value'] += indiv_value              
            if body_type in list(op_js['body_count'].keys()):
                op_js['body_count'][body_type] += 1
                op_js['body_names'][body_type].append(just_name)
            else:
                op_js['body_count'][body_type] = 1
                op_js['body_names'][body_type] = [just_name]           
    op_js['nickname'] = nickname
    op_js['value'] = int(op_js['value'])
    total_value = int(op_js['value'])
    op_js.pop('body_names', None)
    se_data[systemname] = op_js
    with open(final_target, 'w') as target:
        json.dump(se_data, target, indent=4, separators=(',',':'))
    return [op_js, total_value]
