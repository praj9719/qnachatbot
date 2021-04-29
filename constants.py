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

input_text = "query"
output_lang = "out_lang"
output_in_same_lang = "same"

# Bots
science = {
    "name": "Science Bot",
    "database": "bots/science/database",
    "model": "bots/science/model/Science"
}
ssc_science = {
    "name": "SSC Science Bot",
    "database": "bots/ssc_science/database",
    "model": "bots/ssc_science/model/ssc_science"
}
ssc_history = {
    "name": "SSC History Bot",
    "database": "bots/ssc_history/database",
    "model": "bots/ssc_history/model/ssc_history"
}
