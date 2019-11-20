from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "Maliwan"  # 跨域访问
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('Main.html')

def main():
    app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
    main()
