from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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
                lines = self.wrap_text(desc, max_width=500)  # Adjust max_width as needed
                for line in lines:
                    if y_position < 50:
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y_position = text_height
                    c.drawString(50, y_position, line)
                    y_position -= 15

            y_position -= 20  # Additional space after each section

        c.save()
        print("PDF created successfully!")

    def wrap_text(self, text, max_width=500):
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

    def get_text_width(self, text):
        c = canvas.Canvas("tmp.pdf")
        return c.stringWidth(text, "Helvetica", 12)

if __name__ == "__main__":
    from analyze_oop import *
    mapper = DependencyMapper()
    directory_path = '../../additional'  # zmień na ścieżkę do twojego folderu testowego
    mapper.analyze_directory(directory_path)
    raport = Raport()
    raport.create_pdf_from_text(tab_topic, tab_description, "raport.pdf")