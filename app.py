from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health_check():
    return {"status": "healthy"}, 200

@app.route('/gerar-slides-turno')
def gerar_slides_turno():
    return "Slides gerados com sucesso", 200

if __name__ == '__main__':
    app.run(debug=True)