from flask import *
import constants as c
from bot import Bot

app = Flask(__name__)

science_bot = Bot(c.ssc_science)
history_bot = Bot(c.ssc_history)


@app.route('/')
def home():
    res = jsonify({
        c.info: "Question Answer ChatBot",
        c.ssc_science["name"]: "/ssc_science",
        c.ssc_history["name"]: "/ssc_history"
    })
    return res


@app.route('/ssc_science', methods=['GET', 'POST'])
def ssc_science():
    return science_bot.execute(request)


@app.route('/ssc_history', methods=['GET', 'POST'])
def ssc_history():
    return history_bot.execute(request)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
