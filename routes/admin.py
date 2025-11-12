@app.route('/api/admin/knowledge')
def get_knowledge():
    from ai_engine import KNOWLEDGE
    return jsonify(KNOWLEDGE)
