import json

with open('sample-data.json') as file:
    json_data = json.load(file)
    print('''Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------''')
    imdata = json_data['imdata']
    for item in imdata:
        attr = item['l1PhysIf']['attributes']
        dn = attr['dn']
        speed = attr['speed']
        mtu = attr['mtu']

        print(f"{dn:<50}{'':<23}{speed:<8}{mtu:<6}")