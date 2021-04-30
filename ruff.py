# from googletrans import Translator
#
# translator = Translator()
#
#
# def reply(msg):
#     lang = translator.detect(msg).lang
#     response = "He is a scientist"
#     return translator.translate(response, src='en', dest=lang).text
#
#
# def translate(text, dest):
#     try:
#         text = translator.translate(text, src='en', dest=dest).text
#     except ValueError:
#         pass
#     return text
#
#
# def detect_lang(text):
#     return translator.detect(text).lang


# print(detect_lang("who is न्यूटन"))
# print(detect_lang("न्यूटन कोण आहे?"))
# print(translate("who is न्यूटन?", "en"))
# print(reply("न्यूटन कोण आहे?"))

# out = translator.translate("Hello World", src='en', dest='mr').text
# print(out)


# --------------

from wiki import WikiBot
from datetime import datetime
print("start")
t1 = datetime.now()
bot = WikiBot()
t2 = datetime.now()
print(f"Init time: {t2-t1}")
print(bot.ans("who is virat kohli"))
t3 = datetime.now()
print(f"First time: {t3-t2}")
# print(bot.ans("Who is elon musk"))
# t4 = datetime.now()
# print(f"Second time: {t4-t3}")
print("end")
