import json, datetime, sys, math

file = 'habitats.json' 

def carregar():
    try:
        with open(file, 'r') as f: return json.load(f)
    except:
        return {"user": {"level": 1, "xp": 0}, "habits": []}

def salvar(data):
    with open(file, 'w') as f: json.dump(data, f, indent=2)
    atualizar_readme(data)

def atualizar_readme(data):
    # Gera a tabela de hábitos dinamicamente
    tabela = "| Hábito | XP | Status |\n| :--- | :--- | :--- |\n"
    for h in data['habits']:
        check = "✅" if str(datetime.date.today()) in h['history'] else "⬜"
        tabela += f"| {h['name']} | {h['xp_yield']} | {check} |\n"
    
    # Monta o conteúdo do README
    conteúdo = f"""# ⚔️ Habit Quest

![Status](https://img.shields.io/badge/Status-Ativo-brightgreen?style=for-the-badge)

### 📊 Status do Jogador
| Atributo | Valor |
| :--- | :--- |
| **Nível** | ![Level](https://img.shields.io/badge/Level-{data['user']['level']}-blueviolet?style=flat-square) |
| **XP Total** | {data['user']['xp']} |

### 🎯 Missões Diárias
{tabela}

---
*Atualizado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}*
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(conteúdo)

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
