"""
Notes
    - Project - qnachatbot
    - Instance - qcb-instance # External IP - 35.188.169.72
    - Firewall - qcb-firewall # 0.0.0.0/0 Port 5000
    - conda activate qcbenv
    - gunicorn --bind 0.0.0.0:5000 app:app --daemon
    - pkill gunicorn

    - python -m spacy download en_core_web_sm
    - python -m nltk.downloader stopwords
    - python -m nltk.downloader punkt
    - extras -> nginx - qcb_project
"""


API = "http://35.188.169.72:5000/"
methods = ['/science']

# API constants

status = "status"
status_success = "success"
status_failed = "failed"

title = "title"

info = "info"
info_normal = "result ok"

data = "data"
message = "message"

input_text = "message"

# Bots
science = {
    "name": "Science Bot",
    "database": "bots/science/database",
    "model": "bots/science/model/Science"
}