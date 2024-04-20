
class Translate:
    def __init__(self, lang):
        self.lang = lang

    def translate(self, text):
        if self.lang == 'en':
            return text
        if self.lang == 'pl':
            return self.translate_pl(text)
        return text

    def translate_pl(self, text):
        pass