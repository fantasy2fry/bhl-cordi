from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from translator import Translator
from operator import itemgetter
from reportlab.lib.colors import HexColor
from textwrap import wrap
import re


class Raport:
    def create_pdf_from_text(self, tab_topic, tab_description,
                             det_description, det_detailed_descriptor,
                             csrf_description, csrf_detailed_description,
                             insecure_deserialization_description, insecure_deserialization_detailed_description,
                             xss_detector_description, xss_detector_detailed_description, tab_solutions,
                             filename, lang):
        # t = Translator(lang)
        # tab_description = t.translate(tab_description)
        # tab_solutions = t.translate(tab_solutions)
        # tab_topic = t.translate(tab_topic)
        # print(tab_description)

        tab_description_dict = {}
        for topic, desc in zip(tab_topic, tab_description):
            if topic not in tab_description_dict:
                tab_description_dict[topic] = []
            tab_description_dict[topic].append("• " + desc)
        tab_solutions = ["• " + tab_solutions[0], "• " + tab_solutions[1]]
        pos = list(tab_description_dict.keys()).index('Static variable issue')
        items = list(tab_description_dict.items())
        items.insert(pos, ('Solutions', tab_solutions))
        tab_description_dict = dict(items)
        for topic, desc in zip(det_description, list(map(itemgetter(0), det_detailed_descriptor))):
            if topic not in tab_description_dict:
                tab_description_dict[topic] = []
            tab_description_dict[topic].append(desc)
        for topic, desc in zip(csrf_description, list(map(itemgetter(0), csrf_detailed_description))):
            if topic not in tab_description_dict:
                tab_description_dict[topic] = []
            tab_description_dict[topic].append(desc)
        for topic, desc in zip(insecure_deserialization_description, list(map(itemgetter(0), insecure_deserialization_detailed_description))):
            if topic not in tab_description_dict:
                tab_description_dict[topic] = []
            tab_description_dict[topic].append(desc)
        # for topic, desc in zip(xss_detector_description, list(map(itemgetter(0), xss_detector_detailed_description))):
        #     if topic not in tab_description_dict:
        #         tab_description_dict[topic] = []
        #     tab_description_dict[topic].append(desc)

        sections = list(tab_description_dict.items())  # Convert dict items to list of tuples
        self._generate_pdf(sections, filename, tab_solutions)

    def extract_words_from_description(self, tab_description):
        words = re.findall(r"'(\w+)'", tab_description)
        return words

    def _generate_pdf(self, sections, filename, tab_solutions):
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 8)

        text_height = 750
        y_position = text_height

        # Add title to the first page
        c.setFont("Helvetica-Bold", 20)  # Larger font size for the title
        title = "File content analysis"
        c.drawCentredString(letter[0] / 2, y_position, title)
        y_position -= 60

        for topic, descriptions in sections:
            # Check if there's enough space for the section title
            if y_position < 50:
                c.showPage()  # Start a new page
                c.setFillColor(HexColor(0x000000))
                c.setFont("Helvetica", 8)  # Reset font
                y_position = text_height  # Reset y_position

            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(HexColor(0x000000))
            c.drawString(50, y_position, topic)
            y_position -= 20

            if topic == "Solutions":
                c.setFillColor(HexColor(0x0096C7))
                c.setFont("Helvetica", 8)
                for desc in descriptions:
                    lines = self.wrap_text(desc, max_width=500)  # Adjust max_width as needed
                    for line in lines:
                        # Check if there's enough space for the current line
                        if y_position < 50:
                            c.showPage()  # Start a new page
                            c.setFillColor(HexColor(0x0096C7))
                            c.setFont("Helvetica", 8)  # Reset font
                            y_position = text_height  # Reset y_position

                        self.draw_text_with_bold(line, c, y_position)
                        y_position -= 20
            else:
                c.setFillColor(HexColor(0x000000))
                c.setFont("Helvetica", 8)
                for desc in descriptions:
                    lines = self.wrap_text(desc, max_width=500)  # Adjust max_width as needed
                    for line in lines:
                        # Check if there's enough space for the current line
                        if y_position < 50:
                            c.showPage()  # Start a new page
                            c.setFillColor(HexColor(0x000000))
                            c.setFont("Helvetica", 8)  # Reset font
                            y_position = text_height  # Reset y_position

                        self.draw_text_with_bold(line, c, y_position)
                        y_position -= 20

            y_position -= 20  # Additional space after each section

        t = c.beginText()
        t.setTextOrigin(50, 700)
        t.setFont('Helvetica', 8)
        t.setCharSpace(1)
        wraped_text = "\n".join(wrap(tab_solutions[0], 120))
        t.textLines(tab_solutions[0])
        c.showPage()
        c.drawText(t)

        for solution in tab_solutions:
            # Check if there's enough space for the current line
            if y_position < 50:
                c.showPage()  # Start a new page
                c.setFillColor(HexColor(0x0096C7))
                c.setFont("Helvetica", 8)  # Reset font
                y_position = text_height  # Reset y_position
            t.textLines(solution)
            c.drawText(t)

        c.save()
        print("PDF created successfully!")

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            if current_line and self.get_text_width(' '.join(current_line + [word])) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_text_with_bold(self, text, canvas_obj, y_position):
        font = "Helvetica"
        font_size = 8
        bold_font_size = 8
        x_position = 50  # Starting x-coordinate for drawing text

        in_quotes = False
        word_buffer = ""

        for char in text:
            if char == "'":
                if in_quotes:
                    # End of quoted word, draw bold text
                    canvas_obj.setFont(font + "-Bold", bold_font_size)
                    canvas_obj.drawString(x_position, y_position, word_buffer)
                    x_position += canvas_obj.stringWidth(word_buffer, font + "-Bold", bold_font_size)
                    word_buffer = ""
                in_quotes = not in_quotes  # Toggle in_quotes flag
            else:
                if in_quotes:
                    # Inside quoted word, accumulate characters
                    word_buffer += char
                else:
                    # Outside quoted word, draw regular text
                    canvas_obj.setFont(font, font_size)
                    canvas_obj.drawString(x_position, y_position, char)
                    x_position += canvas_obj.stringWidth(char, font, font_size)

        # Draw any remaining text after loop ends
        if word_buffer:
            if in_quotes:
                # Remaining word is in quotes, draw as bold
                canvas_obj.setFont(font + "-Bold", bold_font_size)
            else:
                # Remaining word is not in quotes, draw as regular
                canvas_obj.setFont(font, font_size)
            canvas_obj.drawString(x_position, y_position, word_buffer)

    def get_text_width(self, text):
        c = canvas.Canvas("tmp.pdf")
        return c.stringWidth(text, "Helvetica", 10)


if __name__ == "__main__":
    from analyze_oop import *
    from analyze_vuln import *
    basic_object = BasicAnalyserOOP('../../additional', 1)


    detector = SQLInjectionDetector()
    detector.analyze_directory('../../additional')
    csrf = CSRFDetector()
    csrf.analyze_directory('../../additional')
    insecure_deserialization = InsecureDeserializationDetector()
    insecure_deserialization.analyze_directory('../../additional')
    xss_detector = XSSDetector()
    xss_detector.analyze_directory('../../additional')

    # print("\n")
    # print("\n")
    # print(len(basic_object.tab_solution))
    # print("\n")
    #
    # print(basic_object.tab_solution)


    raport = Raport()
    raport.create_pdf_from_text(basic_object.tab_topic, basic_object.tab_description,
                                detector.description, detector.detailed_description,
                                csrf.description, csrf.detailed_description,
                                insecure_deserialization.description, insecure_deserialization.detailed_description,
                                xss_detector.description, xss_detector.detailed_description, basic_object.tab_solution, "raport.pdf", "en")
