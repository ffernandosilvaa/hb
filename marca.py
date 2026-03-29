import json, datetime, sys, math

file = 'habitats.json' 

def carregar():
    with open(file, 'r') as f: return json.load(f)

def salvar(data):
    with open(file, 'w') as f: json.dump(data, f, indent=2)

def checkin(habit_id):
    data = carregar()
    today = str(datetime.date.today())
    for h in data['habits']:
        if str(h['id']) == str(habit_id) and today not in h['history']:
            h['history'].append(today)
            data['user']['xp'] += h['xp_yield']
            data['user']['level'] = math.floor(data['user']['xp'] / 100) + 1
    salvar(data)

def add_habito(nome, xp):
    data = carregar()
    novo_id = max([h['id'] for h in data['habits']]) + 1 if data['habits'] else 1
    data['habits'].append({"id": novo_id, "name": nome, "xp_yield": int(xp), "history": []})
    salvar(data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            add_habito(sys.argv[2], sys.argv[3])
        else:
            checkin(sys.argv[1])
