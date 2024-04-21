from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

class Raport:
    def create_pdf_from_text(self, tab_topic, tab_description, filename):
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

        # Add title to the PDF document
        c.setFont("Helvetica-Bold", 16)  # Larger font size for the title
        title = "File content analysis"
        c.drawCentredString(letter[0] / 2, y_position, title)
        y_position -= 40

        for topic, descriptions in sections:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, topic)
            y_position -= 20

            c.setFont("Helvetica", 12)
            for desc in descriptions:
                self.draw_text_with_bold(desc, c, y_position)
                y_position -= 15

            y_position -= 20  # Additional space after each section

        c.save()
        print("PDF created successfully!")

    def draw_text_with_bold(self, text, canvas_obj, y_position):
        font = "Helvetica"
        font_size = 12
        bold_font_size = 12
        x_position = 50  # Starting x-coordinate for drawing text

        parts = re.findall(r"'([^']+)'|[^']+", text)

        for part in parts:
            if part.startswith("'") and part.endswith("'"):  # Enclosed in single quotes (to be bold)
                # Set font to bold
                canvas_obj.setFont(font + "-Bold", bold_font_size)
                # Draw the bold text
                canvas_obj.drawString(x_position, y_position, part.strip("'"))
                # Calculate the width of the bold text
                text_width = canvas_obj.stringWidth(part.strip("'"), font + "-Bold", bold_font_size)
            else:
                # Set font to regular
                canvas_obj.setFont(font, font_size)
                # Draw the regular text
                canvas_obj.drawString(x_position, y_position, part)
                # Calculate the width of the regular text
                text_width = canvas_obj.stringWidth(part, font, font_size)

            # Update x_position to move to the end of the drawn text
            x_position += text_width

    def get_text_width(self, text):
        c = canvas.Canvas("tmp.pdf")
        return c.stringWidth(text, "Helvetica", 12)


if __name__ == "__main__":
    from analyze_oop import *
    basic_object = BasicAnalyserOOP('../../additional', 1)
    raport = Raport()
    print("\n")
    print(basic_object.tab_topic)
    print("\n")
    print(basic_object.tab_description)
    print("\n")

    raport.create_pdf_from_text(basic_object.tab_topic, basic_object.tab_description, "raport.pdf")
