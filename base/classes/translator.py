from translate import Translator as TranslateLibTranslator


class Translator:
    def __init__(self, lang):
        self.lang = lang

    def translate(self, text):
        if self.lang == 'en':
            return text
        if self.lang == 'pl':
            return self.translate_pl(text)
        return text

    def translate_pl(self, text_list):
        t = TranslateLibTranslator(to_lang='pl')
        translated_text = []
        for i in range(len(text_list)):
            translated_text.append(t.translate(text_list[i]))
        return translated_text
