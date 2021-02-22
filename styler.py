from invoice import *
from operator import itemgetter, attrgetter

# for SVG support
from svglib.svglib import svg2rlg

# for creating table overlay
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph

# for merging
from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj  



class Styler:
    
    NUM_ROWS = 15
    client_id = ""
    invoice_num = "001"
    invoice_total = '520.00'
    today = "January 22, 2021".upper()
    due_date = ''
    show_due_date = True
    items = []
    materials = []
    materials_total = 0
    labor = 0
    paid = 0
    paypal_amount = 0
    file_name = 'new__pdfTable.pdf'
    background_filename = 'template.pdf'
    pdf = None
    background = None


    def setup_pdf(self):
        self.pdf =  canvas.Canvas(self.file_name, pagesize = letter)
        self.background = pagexobj(PdfReader(self.background_filename,decompress=False).pages[0])
        self.pdf.doForm(makerl(self.pdf, self.background))

    dollar_sign = svg2rlg('Images/Dollar_Sign.svg')
    hours_element = svg2rlg('Images/Hours.svg')

    # Styling
    line_gray = colors.HexColor(0xdddddd)
    dark_gray = colors.HexColor(0x303030)
    light_gray = colors.HexColor(0xe0e0e0)
    white = colors.HexColor(0xFFFFFF)
    blue = colors.HexColor(0x56a6d6)

    pdfmetrics.registerFont(TTFont('Helvetica Neue Bold', 'HelveticaNeue.ttc', subfontIndex=10))
    pdfmetrics.registerFont(TTFont('Helvetica Neue Thin', 'HelveticaNeue.ttc', subfontIndex=3))
    pdfmetrics.registerFont(TTFont('SF Heavy', 'Fonts/SF-UI-Display-Heavy.ttf'))
    pdfmetrics.registerFont(TTFont('SF Black', 'Fonts/SF-UI-Display-Black.ttf'))
    pdfmetrics.registerFont(TTFont('SF Thin', 'Fonts/SF-UI-Display-Thin.ttf'))
    pdfmetrics.registerFont(TTFont('SF Light', 'Fonts/SF-UI-Display-Light.ttf'))

    def make_blue(self, table_id, cell_location):
        table_id.setStyle([
            ('TEXTCOLOR',cell_location, cell_location, self.blue),
        ])

    def make_bold(self, table_id, cell_location):
        table_id.setStyle([
            ('FONTNAME', cell_location, cell_location, 'Helvetica Neue Bold'),
        ])

    def make_centered(self, table_id, cell_location):
        table_id.setStyle([
            ('ALIGN',cell_location, cell_location, 'CENTER'),
        ])
    
    def make_right_aligned(self, table_id, cell_location):
        table_id.setStyle([
            ('ALIGN',cell_location, cell_location, 'RIGHT'),
        ])


    invoice_id_table_data = []
    invoice_id_table = None

    def create_id_table(self):
        # upper right label
        formatted_inv_id = Paragraph(f'''{self.client_id}<font name="SF Thin">{self.invoice_num}</font>''', style=ParagraphStyle('_',
                                fontName="SF Black",
                                textColor=colors.white,
                                fontSize=29.8,
                                alignment=2,
                                spaceAfter=4,
                                    ))

        self.invoice_id_table_data = [
            ['INVOICE'],
            [formatted_inv_id],
            [self.today]
        ]

        self.invoice_id_table = Table(self.invoice_id_table_data, colWidths=[220])

        self.invoice_id_table.setStyle([
            ('TEXTCOLOR',(0,0),(-1,-1), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'SF Black'),
            ('FONTSIZE', (0,0), (-1,0), 13.5),
            # ('FONTSIZE', (0,1), (-1,1), 29.8),
            ('FONTNAME', (0,-1), (-1,-1), 'SF Light'),
            ('FONTSIZE', (0,-1), (-1,-1), 12),
            ('ALIGN',(0,0),(-1,-1),'RIGHT'), 
            # ('GRID',(0,0),(-1,-1),1, colors.black),
            ('TOPPADDING', (0,1), (-1,1), -6),
            ('BOTTOMPADDING', (0,1), (-1,1), 17),
        ])






    data = [['Dates', 'Description', 'Quantity', '', 'Rate', '', 'Cost', '']]
    table = None

    def create_items_table(self):
        materials_row_num = len(self.items) + 2
        
        def add_styles(self, list, table, start_row):
            for num, item in enumerate(list, start_row):
                if 'bold' in item.style:
                    self.make_bold(table, (1, num))
                if 'blue' in item.style:
                    self.make_blue(table, (1, num))
                if 'right' in item.style:
                    self.make_right_aligned(table, (1, num))
                if 'center' in item.style:
                    self.make_centered(table, (1, num))

        q_text = Paragraph(f'''Q - ''', ParagraphStyle('yourtitle',
                                fontName="Helvetica Neue Bold",
                                fontSize=12,
                                alignment=2,
                                spaceAfter=4,
                                textColor = self.dark_gray
                                    ))
        
        def get_item_date_text(self, item):
            if item.beg_date == item.end_date:
                if item.beg_date == None:
                    return ''
                else:
                    return datetime.datetime.strftime(item.beg_date, '%B %d')
            else:
                return datetime.datetime.strftime(item.beg_date, '%b %d') + ' - ' + datetime.datetime.strftime(item.end_date, '%b %d')
                

        def line_hourly(self, item):
            self.data.append([get_item_date_text(self, item), item.item, f'{item.hours:.2f}', self.hours_element, '$', f'{item.rate:.2f}', '$',"{0:,.2f}".format(item.cost)])

        def line_fixed_cost_labor(self, item):
            self.data.append([get_item_date_text(self, item), item.item, '-', self.hours_element, '$', 'Fixed', '$',"{0:,.2f}".format(item.cost)])
            
        def line_fixed_cost(self, item):
            self.data.append([get_item_date_text(self, item), item.item, item.quantity_text, '', item.show_dollar, item.unit_price_text, '$',"{0:,.2f}".format(item.cost)])

        def line_no_marks(self, item):
            self.data.append([get_item_date_text(self, item), item.item, '', '', item.show_dollar, '', '$',"{0:,.2f}".format(item.cost)])




        def add_lines(self, list):
            # populating the data list with items in self.items and self.materials 
            for item in list: 
                if type(item) == Fixed_Item:
                    if list == self.items:
                        if item.quantity < 1:
                            line_no_marks(self, item)
                        else:
                            line_fixed_cost_labor(self, item)
                    elif list == self.materials:
                        line_fixed_cost(self, item) 
                elif type(item) == Hourly_Item:
                    line_hourly(self, item)

        # adding all items
        add_lines(self, self.items)

        # adds a line break
        self.data.append([]) 

        add_lines(self, self.materials)
        
        # print(len(self.items))
        # print(len(self.data))
        # self.data[materials_row_num][0] = 'Materials'
        # print(self.data[materials_row_num])

        
        for _ in range(self.NUM_ROWS - len(self.items) - len(self.materials) - 1):
            self.data.append(['', '', '', '', '', '', '', ''])
        
        # print(len(self.items))
        # print(len(self.data))
        # print(len(self.materials))
        self.data[materials_row_num][0] = 'Materials'
        if len(self.materials) == 0:
            self.data[materials_row_num][1] = 'n/a'
        # print(self.data[materials_row_num])
                
        # Creates table
        self.table = Table(self.data, colWidths=[90,239,41,18,13,40,13,52])

        self.table.setStyle([
            # Property      Beg    End   Property
            # header
            ('TEXTCOLOR',(0,0),(-1,0), self.blue),
            ('ALIGN',(0,0),(-1,0),'CENTER'), 
            ('ALIGN',(1,0),(1,0),'LEFT'), 
            ('FONTNAME', (0,0), (-1,0), 'Helvetica Neue Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 3),
            
            # merging the hours, rate, cost double-cells (because of svgs in unique cells below)
            ('SPAN', (2,0), (3,0)),
            ('SPAN', (4,0), (5,0)),
            ('SPAN', (6,0), (7,0)),

            # main text
            ('TOPPADDING', (0,1), (-1,1), 8),  # first row extra headroom
            ('TEXTCOLOR',(0,1),(-1,-1), self.dark_gray),
            ('FONTNAME', (0,1), (-1,-1), 'SF Thin'),
            ('FONTSIZE', (0,1), (-1,-1), 11),
            ('BOTTOMPADDING', (0,1), (-1,-1), 3.2),
            ('TOPPADDING', (0,2), (-1,-1), 3.05),
            ('ALIGN',(0,1),(0,-1),'CENTER'),  # centers first column
            ('ALIGN',(1,1),(1,-1),'LEFT'),  # left-aligns second column
            ('ALIGN',(2,1),(-1,-1),'RIGHT'),  # right aligns everything from hours to end
            ('RIGHTPADDING', (2,1), (2,-1), 2), # hours cell decrease padding

            # $ signs
            ('FONTNAME', (4,1), (4,-1), 'SF Heavy'),
            ('FONTNAME', (6,1), (6,-1), 'SF Heavy'),
            ('TEXTCOLOR',(4,1), (4,-1), self.light_gray),
            ('TEXTCOLOR',(6,1), (6,-1), self.light_gray),

            # grid lines
            ('LINEABOVE',(0,1),(-1,1),1.5, self.line_gray),  # top line
            ('LINEABOVE',(0,2),(-1,-1),.4, self.line_gray),  # middle lines
            ('LINEBELOW',(0,-1),(-1,-1),1.5, self.line_gray),  # bottom line
            ('LINEBEFORE',(1,1),(2,-1),.4, self.line_gray),  # left lines
            ('LINEBEFORE',(4,1),(4,-1),.4, self.line_gray),  # left lines
            ('LINEBEFORE',(6,1),(6,-1),.4, self.line_gray),  # left lines

            # SVG cell alignment
            # hours icon
            ('BOTTOMPADDING', (3,1), (3,-1), 0),
            ('RIGHTPADDING', (3,1), (3,-1), 0),
            # $ signs
            ('RIGHTPADDING', (4,1), (4,-1), 2),
            ('RIGHTPADDING', (6,1), (6,-1), 2),
            ('LEFTPADDING', (4,1), (4,-1), 0),
            ('LEFTPADDING', (6,1), (6,-1), 0),
        ])

        self.make_blue(self.table, (0, materials_row_num))
        self.make_bold(self.table, (0, materials_row_num))

        add_styles(self, self.items, self.table, 1)
        add_styles(self, self.materials, self.table, len(self.items) + 2)


    # ------------- Totals Table -------------
    totals_table = None

    def create_totals_table(self):
        style = getSampleStyleSheet()
        total_style = ParagraphStyle('yourtitle',
                                fontName="Helvetica Neue Bold",
                                fontSize=21.5,
                                alignment=2,
                                spaceAfter=4,
                                textColor = self.blue
                                    )


        self.totals_table = Table([
            ['Labor', '$', f"{self.labor:,.2f}"],
            ['Materials', '$', f"{self.materials_total:,.2f}"],
            ['Paid', '$', f"{self.paid:,.2f}"],
            [Paragraph(f'''Total  <super rise=7 size=12>$ </super>{self.invoice_total:,.2f}''', total_style)],
            ], colWidths=[100,13,52])

        self.totals_table.setStyle([
            ('TEXTCOLOR',(0,0),(-1,-1),self.dark_gray),
            ('FONTNAME', (0,0), (-1,-1), 'SF Light'),
            ('FONTSIZE', (0,0), (-1,2), 11),
            ('ALIGN',(0,0),(-1,-1),'RIGHT'),  
            # $ padding
            ('RIGHTPADDING', (1,0), (1,-1), 2),
            ('LEFTPADDING', (1,0), (1,-1), 0),
            ('TOPPADDING', (0,1), (-1,2), 6.5),
            ('TOPPADDING', (0,-1), (-1,-1), 10),

            ('FONTNAME', (1,0), (1,-1), 'SF Heavy'),

            ('SPAN', (0,3), (-1,3)),
            ('FONTNAME', (0,3), (-1,3), 'Helvetica Neue Bold'),
            ('FONTSIZE', (0,3), (-1,3), 54),
            ('TEXTCOLOR',(0,3),(-1,3),self.blue),
        ])
    # ------------- END Totals Table -------------
    

    # ------------- Thank you Table -------------
    due_date_data = []
    due_date_table = None
    thank_you_data = []
    thank_you_table = None

    def create_thank_you_table(self):
        line_width = 30 * " "
        
        self.due_date_data = [
            ['',f'PAYMENT DUE BEFORE {self.due_date}',''],
            [line_width, '', line_width],
            ]

        if self.show_due_date == False:
            self.due_date_data[0] = ''

        self.due_date_table = Table(self.due_date_data)

        self.due_date_table.setStyle([
            # ('SPAN', (1,0), (1,1)),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LINEABOVE',(0,1),(-1,1),1.5, self.line_gray), 
            ('FONTNAME', (0,0), (-1,-1), 'SF Heavy'),
            ('FONTSIZE', (0,0), (-1,-1), 8.8),
            ('TEXTCOLOR',(0,0),(-1,-1), self.blue),
            ('RIGHTPADDING', (1,0), (1,0), 10),
            ('LEFTPADDING', (1,0), (1,0), 10),
        ])

        if self.show_due_date == True:
            self.due_date_table.setStyle([
            ('SPAN', (1,0), (1,1)),
        ])

        paragraph_stying = ParagraphStyle('para',
                                fontName="SF Thin",
                                fontSize=10,
                                alignment=1,
                                spaceAfter=40,
                                spaceBefore = 40,
                                textColor = self.dark_gray,
                                leading = 15
                                    )

        above_due_date_text_one = Paragraph(f'''<font name="Helvetica Neue Bold" size="20" color="{self.blue}">Thank you for your business!</font>''', paragraph_stying)

        above_due_date_text_two = Paragraph(f'''Please let us know if you have questions or concerns about this invoice.''', paragraph_stying)

        below_due_date_text = Paragraph(f'''Upon payment of invoice, <font name="Helvetica Neue Bold" color="{self.blue}">above work will be considered accepted & complete</font>. Unless noted in writing 
        that future work is included for this payment, all future work relating to these tasks will be billed separately.''', paragraph_stying)

        self.thank_you_data = [
            [above_due_date_text_one],
            [above_due_date_text_two],
            [self.due_date_table],
            [below_due_date_text]
            ]

        self.thank_you_table = Table(self.thank_you_data, colWidths = [460], rowHeights= [None, None, 20, None])

        self.thank_you_table.setStyle([
            # ('GRID',(0,0),(-1,-1), 1, dark_gray),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,1), (-1,1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BOTTOMPADDING', (0,1), (-1,1), 15),
            ('TOPPADDING', (0,-1), (-1,-1), -6),
        ])

        if self.show_due_date == False:
            self.thank_you_table.setStyle([
                ('BOTTOMPADDING', (0,2), (-1,2), -2),
                ('BOTTOMPADDING', (0,1), (-1,1), 3),
            ])
    # ------------- END Thank you Table -------------

    def draw_on_centered(self, canvas, element, top_padding):
        # places an element on the page centered on the canvas
        centered_x = (canvas._pagesize[0] - element._width)/2
        y = canvas._pagesize[1] - element._height - top_padding
        element.drawOn(self.pdf, centered_x, y)

    def vertical_pad_table_y(self, canvas, table_one, table, padding):
        # places a table on canvas based off height of item table
        x = canvas._pagesize[0] - table._width - 53.2
        y = canvas._pagesize[1] - table_one._height - table._height - 139 - padding
        table.drawOn(canvas, x, y)

    def add_to_canvas(self):
        # Adds everything to the canvas

        # adds paypal amount to bottom right
        self.pdf.setFont('SF Black', 6.88)
        self.pdf.setFillColor(colors.white)
        self.pdf.drawString(510,20.5, f"${self.paypal_amount:,.2f}")

        # Adds all of the tables to the canvas
        self.invoice_id_table.wrapOn(self.pdf, 0, 0)
        self.invoice_id_table.hAlign = 'LEFT'
        self.invoice_id_table.drawOn(self.pdf, 344, self.pdf._pagesize[1] -90)
        self.table.wrapOn(self.pdf, 0, 0)
        self.totals_table.wrapOn(self.pdf, 0, 0)
        self.table.hAlign = 'CENTER'
        self.draw_on_centered(self.pdf, self.table, 139)
        self.vertical_pad_table_y(self.pdf, self.table, self.totals_table, 10)
        self.thank_you_table.wrapOn(self.pdf, 0, 0)
        self.draw_on_centered(self.pdf, self.thank_you_table, self.pdf._pagesize[1] - self.thank_you_table._height - 115)

        
    def save_pdf(self):
        # renders and saves PDF
        self.pdf.showPage() 
        self.pdf.save()

    def __init__(self, output_filename, invoice, background_pdf = 'template.pdf', show_due_date = True):
        for item in invoice.items:
            self.items.append(item)
        
        for material in invoice.materials:
            self.materials.append(material)

        
        self.client_id = invoice.cust_id.upper()
        self.invoice_num = f'{invoice.number:03d}'
        self.invoice_total = invoice.total
        self.today = invoice.date.upper()
        self.due_date = invoice.due_date.upper()
        self.show_due_date = show_due_date
        self.materials_total = invoice.total_materials
        self.labor = invoice.total_labor
        self.paid = invoice.total_paid
        self.paypal_amount = invoice.paypal_due

        self.file_name = output_filename
        self.background_filename = background_pdf

        self.setup_pdf()

        # create tables from above
        self.create_id_table()        
        self.create_items_table()
        self.create_totals_table()
        self.create_thank_you_table()

        self.add_to_canvas()


if __name__ == '__main__':
    # item_one = Fixed_Item(450, "this is an item name", date = "Dec 14", style='right, bold, blue')
    # item_two = Hourly_Item(25.5, 50, "this is an item", date = "Dec 4")
    # item_three = Fixed_Item(45.50, "this is an item", date = "Dec 4")
    # item_four = Fixed_Item(5, "Some Discount", date = "Dec 14", style='right, bold, blue', quantity = -1)


    # mat_one = Fixed_Item(50, 'some item')
    # mat_two = Fixed_Item(22.50, "Music")
    # mat_three = Fixed_Item(-550, "Some Discount", quantity = 0, style='right, bold')


    # test_invoice = Invoice("BLAH", 15)
    # test_invoice.add_items(item_one, item_two, item_three, item_four)
    # test_invoice.add_materials(mat_one, mat_two, mat_three)
    # styler = Styler('pdfTable.pdf', test_invoice, show_due_date=True)
    pass