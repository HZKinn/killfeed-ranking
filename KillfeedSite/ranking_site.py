from flask import Flask, render_template_string, request
import sqlite3

DB = "ranking.db"
app = Flask(__name__)

def query(sql, args=()):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql, args)
    data = cur.fetchall()
    conn.close()
    return data

TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Ranking Killfeed</title>
<style>
    body {
        background: #0a0f1a;
        color: #c7d8ff;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
    }
    h1, h2 {
        color: #5da8ff;
        text-shadow: 0 0 5px #1b4d8f;
    }
    .container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        background: #111a2e;
        border-radius: 10px;
        box-shadow: 0 0 15px #0e3a6d;
    }
    .card {
        padding: 10px;
        margin: 10px 0;
        background: #0d1424;
        border-left: 4px solid #5da8ff;
        border-radius: 6px;
    }
    a {
        color: #74b2ff;
        text-decoration: none;
    }
    input, button, select {
        padding: 8px;
        border-radius: 6px;
        border: none;
        background: #0c1a33;
        color: #c7d8ff;
    }
    button {
        cursor: pointer;
        background: #124a99;
    }
</style>
</head>
<body>
<div class="container">
    <h1>Ranking — Killfeed</h1>

    <h2>Pesquisar Jogador</h2>
    <form method="get" action="/player">
        <input type="text" name="nome" placeholder="Nome do jogador" required>
        <button type="submit">Buscar</button>
    </form>
    <br>

    <h2>Top Killers</h2>
    {% for k,c in killers %}
        <div class="card">{{k}} — <b>{{c}}</b> kills</div>
    {% endfor %}

    <h2>Quem mais morreu</h2>
    {% for v,c in deaths %}
        <div class="card">{{v}} — <b>{{c}}</b> mortes</div>
    {% endfor %}

    <h2>Pesquisar Jogador</h2>
    <form method="get" action="/player">
        <input type="text" name="nome" placeholder="Nome do jogador" required>
        <button type="submit">Buscar</button>
    </form>
</div>
</body>
</html>
"""

PLAYER_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>{{player}} — Detalhes</title>
<style>
    body { background:#0a0f1a; color:#c7d8ff; font-family:Arial; padding:20px; }
    h1 { color:#5da8ff; }
    .card{ background:#111a2e; padding:10px; margin:10px 0; border-radius:8px; }
</style>
</head>
<body>
<h1>Jogador: {{player}}</h1>

<h2>Quem ele mais matou</h2>
{% for v,c in matou %}
<div class="card">{{player}} matou <b>{{v}}</b> — {{c}} vezes</div>
{% endfor %}

<h2>Quem mais matou ele</h2>
{% for k,c in morreu %}
<div class="card"><b>{{k}}</b> matou {{player}} — {{c}} vezes</div>
{% endfor %}

<a href="/">← Voltar</a>
</body>
</html>
"""

@app.route("/")
def home():
    killers = query("SELECT killer, COUNT(*) FROM kills GROUP BY killer ORDER BY 2 DESC LIMIT 20")
    deaths = query("SELECT victim, COUNT(*) FROM kills GROUP BY victim ORDER BY 2 DESC LIMIT 20")
    return render_template_string(TEMPLATE, killers=killers, deaths=deaths)

@app.route("/player")
def player():
    nome = request.args.get("nome", "").strip()
    if not nome:
        return "Nome inválido"

    matou = query("SELECT victim, COUNT(*) FROM kills WHERE killer = ? GROUP BY victim ORDER BY 2 DESC", (nome,))
    morreu = query("SELECT killer, COUNT(*) FROM kills WHERE victim = ? GROUP BY killer ORDER BY 2 DESC", (nome,))

    return render_template_string(PLAYER_TEMPLATE, player=nome, matou=matou, morreu=morreu)

app.run(port=5000, debug=False)
