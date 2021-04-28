from flask import *
import constants as c
from bot import Bot

app = Flask(__name__)

science_bot = Bot(c.science)


@app.route('/')
def home():
    return jsonify({c.info: "Question Answer ChatBot"})


@app.route('/science', methods=['GET', 'POST'])
def science():
    return science_bot.execute(request)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=False)
