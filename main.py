from flask import Flask, render_template
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
babel = Babel(app)
app.config['BABEL_LANGUAGES'] = ['en', 'ru']


@app.route('/')
def main_page():
    return render_template('main_page.html', title=_l("Main Page"))


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
