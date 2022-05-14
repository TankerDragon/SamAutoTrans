# pdf.set_font("helvetica", size=10)
# fpdf.multi_cell(w: float, h: float, txt: str, border = 0, align: str = 'J', fill: bool = False)
# fpdf.set_font(family, style = '', size = 0)
# A4 is a paper size 210 millimeters wide and 297 millimeters long.
from msilib.schema import tables
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
table_padding = 1

def certre_of_page(s):
    return page_width/2 - pdf.get_string_width(s)/2

def right_of(s):
    return page_width - pdf.get_string_width(s) - padding

def left_in_table(s):
    return padding + table_padding

def centre_in_table(s):
    return page_width/2 + table_padding

pdf = FPDF()
pdf.add_page()
pdf.set_fill_color(100,100,235)

# pdf.cell(w=190, h=8, txt="DRIVER'S DAILY LOG\n", border=0, align='C',fill=True)
# pdf.cell(w=190, h=8, txt="Friday May 13th 2022", border=0, align='C',fill=True)
s = "DRIVER'S DAILY LOG"
pdf.set_font("helvetica", style='B', size=15)
pdf.text(certre_of_page(s),15,s)

s = "Friday May 13th 2022"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(certre_of_page(s), 19,s)

s = "USA Property 70 hour / 8 day"
pdf.set_font("helvetica", size=6)
pdf.text(right_of(s), 17, s)

table_start = 25
x = table_start

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Driver"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "ALISHER AKHMEDOV"
pdf.set_font("helvetica", size=8)
pdf.text(certre_of_page(s), x,s)

x+= 1

pdf.line(padding, x, page_width- padding, x)


x+= 3

s = "Driver ID"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "AKH290921"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "ST"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "New york"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

#####################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Co-Drivers (ID)"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

#####################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "DL Number"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "UP245413"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "Time Zone"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "EDT"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

#####################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "ELD ID"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "4AWJ"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "Time Zone Offset"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "UTC-4"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

#####################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "ELD Provider"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "TitTi ELD Inc"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "24 Period Starting Time"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "Midnight"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

#####################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Carrier"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "SAM AUTO TRANS LLC"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "Vehicles (VIN)"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "000101 (4V4NC9EH7MN229000)"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

#####################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "USDOT #"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "2520572"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "Exempt Driver Status"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "NO"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Main Office"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "1900 ENTERPRISE PKWY SUITE B"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "Trailers"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "Bobtail, GV2202235"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

x+= 3

s = "TWINSBURG, OH 44087"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Home Terminal"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "1900 ENTERPRISE PKWY SUITE B"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

s = "Distance"
pdf.set_font("helvetica",  style='B', size=8)
pdf.text(centre_in_table(s), x,s)

s = "86 mi"
pdf.set_font("helvetica", size=8)
pdf.text(centre_in_table(s) + 40, x,s)

x+= 3

s = "TWINSBURG, OH 44087"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 40, x,s)

######################
######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Shipping Docs"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "None, Empty trailer"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 50, x,s)

######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Malfunction Indicators"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "NO"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 50, x,s)

######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Data Diagnostic Indicators"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "NO"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 50, x,s)

######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Current Location"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = ""
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 50, x,s)

######################
x+= 1

pdf.line(padding, x, page_width- padding, x)

x+= 3

s = "Unidentified Driver Records"
pdf.set_font("helvetica", style='B', size=8)
pdf.text(left_in_table(s), x,s)

s = "0"
pdf.set_font("helvetica", size=8)
pdf.text(left_in_table(s) + 50, x,s)

#######################
x+= 1

pdf.line(padding, x, page_width- padding, x)
######################
pdf.line(padding, table_start, padding, x) #left side of table
pdf.line(page_width- padding, table_start, page_width- padding, x) #right side of table
######################

x+= 10
# fpdf.image(name, x = None, y = None, w = 0, h = 0, type = '', link = '')
pdf.image("../static/images/graph_day.jpg", x = padding, y = x, w= page_width - 2*padding)

pdf.output('reports/test.pdf')
