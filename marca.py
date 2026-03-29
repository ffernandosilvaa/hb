import json, datetime, sys, math

file = 'habitos.json'
habit_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

with open(file, 'r+') as f:
    data = json.load(f)
    today = str(datetime.date.today())
    
    for h in data['habits']:
        if h['id'] == habit_id and today not in h['history']:
            h['history'].append(today)
            data['user']['xp'] += h['xp_yield']
            # Formula: Level 1 = 0 XP, Level 2 = 100 XP, Level 3 = 400 XP...
            data['user']['level'] = math.floor(math.sqrt(data['user']['xp'] / 25)) + 1
            
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
