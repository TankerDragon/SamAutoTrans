# pdf.set_font("helvetica", size=10)
# fpdf.multi_cell(w: float, h: float, txt: str, border = 0, align: str = 'J', fill: bool = False)
# fpdf.set_font(family, style = '', size = 0)
# A4 is a paper size 210 millimeters wide and 297 millimeters long.
from fpdf import FPDF

data = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Carlson", "Banks", "19", "Los Angeles"),
    ("Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire"),
)

page_width = 210
page_height = 297
padding = 15

def certre_of(s):
    return page_width/2 - pdf.get_string_width(s)/2

def right_of(s):
    return page_width - pdf.get_string_width(s) - padding

pdf = FPDF()
pdf.add_page()
pdf.set_fill_color(100,100,235)

# pdf.cell(w=190, h=8, txt="DRIVER'S DAILY LOG\n", border=0, align='C',fill=True)
# pdf.cell(w=190, h=8, txt="Friday May 13th 2022", border=0, align='C',fill=True)
s = "DRIVER'S DAILY LOG"
pdf.set_font("helvetica", style='B', size=15)
pdf.text(certre_of(s),15,s)

s = "Friday May 13th 2022"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(certre_of(s), 19,s)

s = "USA Property 70 hour / 8 day"
pdf.set_font("helvetica", size=6)
pdf.text(right_of(s), 17, s)

pdf.line(padding, 25, page_width- padding, 25)

s = "Friday May 13th 2022"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(certre_of(s), 19,s)

pdf.output('reports/test.pdf')
