from googletrans import Translator

translator = Translator()


def reply(msg):
    lang = translator.detect(msg).lang
    response = "He is a scientist"
    return translator.translate(response, src='en', dest=lang).text


def translate(text, dest):
    try:
        text = translator.translate(text, src='en', dest=dest).text
    except ValueError:
        pass
    return text


def detect_lang(text):
    return translator.detect(text).lang


# print(detect_lang("who is न्यूटन"))
# print(detect_lang("न्यूटन कोण आहे?"))
# print(translate("who is न्यूटन?", "en"))
# print(reply("न्यूटन कोण आहे?"))

out = translator.translate("Hello World", src='en', dest='mr').text
print(out)
