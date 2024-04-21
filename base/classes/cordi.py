from analyze_oop import *
from generate_employee_plots import *
from raport import Raport
from analyze_vuln import SQLInjectionDetector, CSRFDetector, XSSDetector, InsecureDeserializationDetector
import uuid


class Cordi:
    def __init__(self, folder, lang, type_of_report="basic_report"):
        self.folder = folder
        self.text = []
        self.lang = lang
        self.type_of_report = type_of_report

        # Upewnij się, że ścieżka prowadzi do pliku CSV
        if not os.path.isfile(self.folder):
            print(f"Podana ścieżka '{self.folder}' nie jest plikiem. Ustawiam domyślny plik CSV.")
            self.folder = '../../additional/default_data.csv'  # Zakładamy, że istnieje domyślny plik CSV

    def get_mac_address(self):
        # Pobiera unikalny adres MAC urządzenia
        mac = uuid.getnode()
        return ':'.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))

    def run(self):
        if self.type_of_report == "basic_report":
            basic_object = BasicAnalyserOOP(self.folder, self.get_mac_address())

            detector = SQLInjectionDetector()
            detector.analyze_directory(self.folder)
            csrf = CSRFDetector()
            csrf.analyze_directory(self.folder)
            insecure_deserialization = InsecureDeserializationDetector()
            insecure_deserialization.analyze_directory(self.folder)
            xss_detector = XSSDetector()
            xss_detector.analyze_directory(self.folder)

            raport = Raport()
            raport.create_pdf_from_text(basic_object.tab_topic, basic_object.tab_description,
                                        detector.description, detector.detailed_description,
                                        csrf.description, csrf.detailed_description,
                                        insecure_deserialization.description, insecure_deserialization.detailed_description,
                                        xss_detector.description, xss_detector.detailed_description, "raport.pdf", "en")

        elif self.type_of_report == "plot_report":

            plot_generator = GenerateEmployeePlots(self.get_mac_address(), '../../data/user_analysis.csv')


            #plot_generator.load_data()
            #plot_generator.create_combined_plot()


cordi = Cordi('../../additional', "en", "basic_report")

cordi.run()
