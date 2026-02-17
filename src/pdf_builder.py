"""PDF generation module for certification prep books using fpdf2."""

import os
import textwrap
from datetime import datetime
from fpdf import FPDF

FONT_REGULAR = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"


class CertPDF(FPDF):
    """Custom PDF class for certification prep books."""

    def __init__(self, cert_name: str):
        super().__init__()
        self.cert_name = cert_name
        self._setup_fonts()
        self.set_auto_page_break(auto=True, margin=25)

    def _setup_fonts(self):
        self.add_font("NanumGothic", "", FONT_REGULAR)
        self.add_font("NanumGothic", "B", FONT_BOLD)

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("NanumGothic", "B", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self.cert_name + " 대비서", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-20)
        self.set_font("NanumGothic", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")

    def add_cover_page(self):
        """Generate the cover page."""
        self.add_page()
        self.ln(60)

        # Title
        self.set_font("NanumGothic", "B", 32)
        self.set_text_color(30, 60, 120)
        self.cell(0, 20, self.cert_name, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

        # Subtitle
        self.set_font("NanumGothic", "B", 20)
        self.set_text_color(60, 60, 60)
        self.cell(0, 15, "자격증 시험 대비서", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

        # Decorative line
        self.set_draw_color(30, 60, 120)
        self.set_line_width(1)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(15)

        # Description
        self.set_font("NanumGothic", "", 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, "핵심 이론 + 기출문제 + 상세 해설", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(40)

        # Date
        self.set_font("NanumGothic", "", 10)
        self.set_text_color(130, 130, 130)
        today = datetime.now().strftime("%Y년 %m월 %d일")
        self.cell(0, 10, f"생성일: {today}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "Gemini AI 기반 자동 생성", align="C", new_x="LMARGIN", new_y="NEXT")

    def add_toc_page(self, outline: str):
        """Generate the table of contents page."""
        self.add_page()
        self._section_title("목 차")
        self.ln(5)

        self.set_text_color(40, 40, 40)
        for line in outline.strip().split("\n"):
            stripped = line.strip()
            if not stripped:
                self.ln(3)
                continue
            if stripped.startswith("제") and "장" in stripped[:5]:
                self.ln(3)
                self.set_font("NanumGothic", "B", 12)
                self.cell(0, 8, stripped, new_x="LMARGIN", new_y="NEXT")
            else:
                self.set_font("NanumGothic", "", 10)
                self.cell(0, 7, "    " + stripped, new_x="LMARGIN", new_y="NEXT")

    def add_theory_section(self, chapter_title: str, content: str):
        """Add a theory chapter to the PDF."""
        self.add_page()
        self._section_title(chapter_title)
        self.ln(3)
        self._write_body(content)

    def add_questions_section(self, content: str):
        """Add practice exam questions section."""
        self.add_page()
        self._section_title("기출문제 및 모의고사")
        self.ln(3)
        self._write_body(content)

    def add_answers_section(self, content: str):
        """Add answer key section."""
        self.add_page()
        self._section_title("정답 및 해설")
        self.ln(3)
        self._write_body(content)

    def _section_title(self, title: str):
        """Render a styled section title."""
        self.set_font("NanumGothic", "B", 18)
        self.set_text_color(30, 60, 120)
        self.cell(0, 15, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 60, 120)
        self.set_line_width(0.5)
        y = self.get_y()
        self.line(10, y, 200, y)
        self.ln(8)

    def _write_body(self, content: str):
        """Write body text with basic formatting support."""
        self.set_text_color(30, 30, 30)
        effective_width = self.w - self.l_margin - self.r_margin

        for line in content.split("\n"):
            stripped = line.strip()

            if not stripped:
                self.ln(4)
                continue

            # Sub-section headers in [brackets]
            if stripped.startswith("[") and stripped.endswith("]"):
                self.ln(4)
                self.set_font("NanumGothic", "B", 13)
                self.set_text_color(40, 80, 140)
                self.multi_cell(effective_width, 8, stripped[1:-1])
                self.set_text_color(30, 30, 30)
                self.ln(2)
                continue

            # Emphasized text in <<brackets>>
            if "<<" in stripped and ">>" in stripped:
                self.set_font("NanumGothic", "B", 11)
                text = stripped.replace("<<", "").replace(">>", "")
                self.multi_cell(effective_width, 7, text)
                self.set_font("NanumGothic", "", 10)
                continue

            # Question headers (문제 N.)
            if stripped.startswith("문제 ") and "." in stripped[:8]:
                self.ln(4)
                self.set_font("NanumGothic", "B", 11)
                self.multi_cell(effective_width, 7, stripped)
                self.set_font("NanumGothic", "", 10)
                continue

            # Answer headers (정답:)
            if "정답:" in stripped[:10] or "정답 :" in stripped[:10]:
                self.ln(3)
                self.set_font("NanumGothic", "B", 11)
                self.set_text_color(0, 100, 0)
                self.multi_cell(effective_width, 7, stripped)
                self.set_text_color(30, 30, 30)
                self.set_font("NanumGothic", "", 10)
                continue

            # Key concept summary
            if stripped.startswith("핵심 개념:") or stripped.startswith("핵심개념:"):
                self.set_font("NanumGothic", "B", 10)
                self.set_text_color(150, 80, 0)
                self.multi_cell(effective_width, 7, stripped)
                self.set_text_color(30, 30, 30)
                self.set_font("NanumGothic", "", 10)
                self.ln(2)
                continue

            # Regular body text
            self.set_font("NanumGothic", "", 10)
            self.multi_cell(effective_width, 7, stripped)

    def save(self, output_dir: str = "output") -> str:
        """Save the PDF and return the file path."""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self.cert_name.replace(" ", "_").replace("/", "_")
        filename = f"{safe_name}_대비서_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)
        self.output(filepath)
        return filepath
