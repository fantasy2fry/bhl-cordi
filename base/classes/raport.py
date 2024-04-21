from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from translator import Translator
import re


class Raport:
    def create_pdf_from_text(self, tab_topic, tab_description, filename, lang):
        tab_description_dict = {}
        for topic, desc in zip(tab_topic, tab_description):
            if topic not in tab_description_dict:
                tab_description_dict[topic] = []
            tab_description_dict[topic].append(desc)
        sections = list(tab_description_dict.items())  # Convert dict items to list of tuples
        self._generate_pdf(sections, filename)

    def _generate_pdf(self, sections, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 12)

        text_height = 750
        y_position = text_height

        # Add title to the first page
        c.setFont("Helvetica-Bold", 20)  # Larger font size for the title
        title = "File content analysis"
        c.drawCentredString(letter[0] / 2, y_position, title)
        y_position -= 60

        c.setFont("Helvetica-Bold", 16)  # Larger font size for the title
        title = "OOP oriented analysis"
        c.drawCentredString(letter[0] / 2, y_position, title)
        y_position -= 40

        for topic, descriptions in sections:
            # Check if there's enough space for the section title
            if y_position < 50:
                c.showPage()  # Start a new page
                c.setFont("Helvetica", 12)  # Reset font
                y_position = text_height  # Reset y_position

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, topic)
            y_position -= 20

            c.setFont("Helvetica", 12)
            for desc in descriptions:
                lines = self.wrap_text(desc, max_width=500)  # Adjust max_width as needed
                for line in lines:
                    # Check if there's enough space for the current line
                    if y_position < 50:
                        c.showPage()  # Start a new page
                        c.setFont("Helvetica", 12)  # Reset font
                        y_position = text_height  # Reset y_position

                    self.draw_text_with_bold(line, c, y_position)
                    y_position -= 15

            y_position -= 20  # Additional space after each section

        c.setFont("Helvetica-Bold", 16)  # Larger font size for the title
        title = "Vulnerabilities oriented analysis"
        c.drawCentredString(letter[0] / 2, y_position, title)
        y_position -= 40

        c.save()
        print("PDF created successfully!")

    def wrap_text(self, text, max_width):
        import math
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
        font_size = 12
        bold_font_size = 12
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
        return c.stringWidth(text, "Helvetica", 12)


if __name__ == "__main__":
    from analyze_oop import *
    basic_object = BasicAnalyserOOP('../../additional', 1)
    raport = Raport()

    print(basic_object.tab_description)

    raport.create_pdf_from_text(basic_object.tab_topic, basic_object.tab_description, "raport.pdf", "ru")
