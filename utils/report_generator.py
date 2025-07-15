from fpdf import FPDF
import os

class MatchReportPDF(FPDF):
    def header(self):
        if os.path.exists("assets/logo.png"):
            self.image("assets/logo.png", 10, 8, 33)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "AI Resume Match Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_match_content(self, match_score, matched_skills):
        self.set_font("Arial", "", 12)
        self.ln(20)
        self.multi_cell(0, 10, f"Match Score: {match_score}%")
        self.ln(5)
        self.multi_cell(0, 10, f"Matched Skills:\n{', '.join(matched_skills)}")

def generate_match_report(match_score, matched_skills, filename="reports/match_report.pdf"):
    pdf = MatchReportPDF()
    pdf.add_page()
    pdf.add_match_content(match_score, matched_skills)
    pdf.output(filename)
    return filename
