from translate import Translator as TranslateLibTranslator


class Translator:
    def __init__(self, lang):
        self.lang = lang

    def translate(self, text_list, lang):
        t = TranslateLibTranslator(to_lang=lang)
        translated_text = []
        for i in range(len(text_list)):
            translated_text.append(t.translate(text_list[i]))
        return translated_text
