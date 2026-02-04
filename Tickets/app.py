import mysql.connector
import json
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'projeto_final_github'

# --- CONEXÃO MYSQL ---
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",  # <-- Introduz a tua senha aqui
        database="sistema_tickets"
    )

# --- ROTAS ---

@app.route('/')
def pagina_inicial():
    status_filtro = request.args.get('status', 'todos')
    busca = request.args.get('busca', '')

    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    
    if status_filtro != 'todos':
        query += " AND status = %s"
        params.append(status_filtro)
    if busca:
        query += " AND (assunto LIKE %s OR solicitante LIKE %s)"
        params.append(f"%{busca}%")
        params.append(f"%{busca}%")

    query += " ORDER BY data_abertura DESC"
    cursor.execute(query, params)
    tickets = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/criar', methods=['POST'])
def criar_ticket():
    solicitante = request.form['solicitante']
    assunto = request.form['assunto']
    problema = request.form['problema']
    
    conn = conectar_db()
    cursor = conn.cursor()
    sql = "INSERT INTO tickets (solicitante, assunto, problema, comentarios) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (solicitante, assunto, problema, json.dumps([])))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pagina_inicial'))

@app.route('/ticket/<int:ticket_id>')
def detalhe_ticket(ticket_id):
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE id_ticket = %s", (ticket_id,))
    ticket = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if ticket:
        ticket['comentarios'] = json.loads(ticket['comentarios'])
        return render_template('detalhes.html', ticket=ticket)
    return "Ticket não encontrado", 404

@app.route('/ticket/<int:ticket_id>/atualizar', methods=['POST'])
def atualizar_ticket(ticket_id):
    novo_status = request.form.get('status')
    responsavel = request.form.get('responsavel') or 'Não Atribuído'

    conn = conectar_db()
    cursor = conn.cursor()
    sql = "UPDATE tickets SET status = %s, responsavel = %s WHERE id_ticket = %s"
    cursor.execute(sql, (novo_status, responsavel, ticket_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('detalhe_ticket', ticket_id=ticket_id))

@app.route('/ticket/<int:ticket_id>/comentar', methods=['POST'])
def adicionar_comentario(ticket_id):
    autor = request.form['autor']
    texto = request.form['texto']
    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT comentarios FROM tickets WHERE id_ticket = %s", (ticket_id,))
    resultado = cursor.fetchone()
    
    comentarios = json.loads(resultado['comentarios'])
    comentarios.append({"autor": autor, "texto": texto, "data": data})
    
    cursor.execute("UPDATE tickets SET comentarios = %s WHERE id_ticket = %s", (json.dumps(comentarios), ticket_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('detalhe_ticket', ticket_id=ticket_id))

@app.route('/ticket/<int:ticket_id>/deletar', methods=['POST'])
def deletar_ticket(ticket_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id_ticket = %s", (ticket_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pagina_inicial'))

if __name__ == '__main__':
    app.run(debug=True)