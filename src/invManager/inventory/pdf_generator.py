import random
import os
from pathlib import Path
from numpy import product
from numpy.core.fromnumeric import prod

from pandas.core.algorithms import quantile
from tqdm import tqdm
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab.lib.pagesizes
from django.http import HttpResponse, response
from .models import PurchaseOrder,PurchaseProduct
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.pdfbase.pdfmetrics import stringWidth

from textwrap import wrap
from barcode import EAN13

def create_barcode(code):
    my_code = EAN13(code)
    my_code.save(code)
    return code, my_code


YU_GOTHIC = Path(filter(lambda n: (Path(n) / "Fonts" / "YuGothB.ttc").exists(), os.environ.get("PATH").split(";")).__next__()) / "Fonts" / "YuGothB.ttc"

def make_pdf_file(purchase_order):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "somefilename.pdf"'

    
    vendor = purchase_order.vendor
    dv_date =purchase_order.delivery_date
    products = purchase_order.products.all()
    A7 = reportlab.lib.pagesizes.A7
    #Create a PDF with text
    # c = canvas.Canvas("base.pdf", pagesize=A7)
    c = canvas.Canvas(response)
    c.setPageSize((300,300))
    # pdfmetrics.registerFont(TTFont("YU", YU_GOTHIC))
    # c.setFont('YU', 20)
    for p_product in products:
        quantity = p_product.quantity
        pack = p_product.pack
        measure_unit = p_product.measure_unit
        box_number = p_product.box_number
        product_name = p_product.product.name
        product_id = p_product.product.id
        barcode_name, my_code = create_barcode(str(box_number)+('0'*(12-len(str(box_number)))))
        barcode_name += '.svg'
        barcode_img = svg2rlg(barcode_name)
        # c.drawInlineImage(barcode_img, 5, A7[1]-250, 295,A7[1]-250)
       
        for i in range(1,quantity+1): 
            renderPDF.draw(barcode_img,c, 80,30)
            pdfmetrics.registerFont(TTFont("YU", YU_GOTHIC))
            c.setFont('YU', 20)
            # delivery date and measuring
            c.drawString(20, A7[1] - 30, f" {dv_date}    {measure_unit} X {pack}")
            # vendor name
            c.setFont('YU', 18)
            c.drawString(10, A7[1] - 60, f" {vendor} ")
            c.line(0,A7[1]-65, 300, A7[1]-65)
            # t = c.beginText()
            # t.setFont('YU',20)
            # t.setTextOrigin(25,A7[1]-65)
            # wraped_name = "\n".join(wrap(vendor.name,25))
            # t.textLines(wraped_name)
            # c.drawText(t)
            #box number
            c.setFont('YU', 20)
            c.drawString(110, A7[1] - 95, f" {box_number}")
            #number of boxes
            c.drawString(110, A7[1] - 125, f" {i} of {quantity} ")
            c.line(0,A7[1]-130, 300, A7[1]-130)

            #flower name
            t = c.beginText()
            t.setFont('YU', 25)
            t.setTextOrigin(25,140)
            wraped_text = "\n".join(wrap(product_name,20))
            t.textLines(wraped_text)
            c.drawText(t)

            # c.drawString(30, A7[1]-165, f'{product_name}')
            c.line(0,A7[1]-200, 300, A7[1]-200)
            c.line(0,A7[1]-200, 300, A7[1]-200)
            c.showPage()
        # c.showPage()
        # c.drawInlineImage(APP_ROOT + "/static/footer_image.png", inch*.25, inch*.25, PAGE_WIDTH-(.5*inch), (.316*inch))

        # c.rect(0, 0, A7[0], A7[1])
        p_product.barcode = my_code
        p_product.save()
    c.save()

    return response

    # Create Page
    # with open("base.pdf", mode="rb") as f:
    #     r = PdfFileReader(f)
    #     p = writer.addBlankPage(300, 300)
        # scale = [a / b for a, b in zip(size, A7)]
        # p.mergeTransformedPage(r.getPage(0), [scale[0], 0, 0 , scale[1], 0, 0] , True)

def make_pdf_on_canvas(c, po, page_size):

    vendor = po.vendor
    dv_date = po.delivery_date
    products = po.products.all()
    print(vendor)
    for product in products:
        barcode_name = str(product.box_number)+('0'*(12-len(str(product.box_number))))
        barcode, my_code = create_barcode(barcode_name)
        barcode += '.svg'
        print(my_code)

        barcode_img = svg2rlg(barcode)

        quantity =product.quantity
        pack =product.pack
        measure_unit =product.measure_unit
        box_number = product.box_number
        product_name = product.product.name
        product_id = product.product.id

        for i in range(1, product.quantity +1):
            renderPDF.draw(barcode_img,c,80,30)
            pdfmetrics.registerFont(TTFont("YU", YU_GOTHIC))
            c.setFont('YU', 20)
            c.drawString(20, page_size - 30, f" {dv_date}    {measure_unit} X {pack}")

            c.setFont('YU', 18)
            c.drawString(10, page_size - 60, f" {vendor} ")
            c.line(0,page_size-65, 300, page_size-65)

            c.setFont('YU', 20)
            c.drawString(110, page_size - 95, f" {box_number}")

            c.drawString(110, page_size - 125, f" {i} of {quantity} ")
            c.line(0,page_size-130, 300, page_size-130)

            t = c.beginText()
            t.setFont('YU', 25)
            t.setTextOrigin(25,140)
            wraped_text = '\n'.join(wrap(product_name,20))
            t.textLines(wraped_text)
            c.drawText(t)

            c.line(0,page_size-200, 300, page_size-200)
            c.line(0,page_size-200, 300, page_size-200)
            c.showPage()
        product.barcode = my_code
        product.save()



def make_pdf_pos_by_date(pos):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "labels.pdf"'

    c = canvas.Canvas(response)
    c.setPageSize((300,300))
    page_size = reportlab.lib.pagesizes.A7

    for po in pos:
        make_pdf_on_canvas(c,po, page_size[1])
    
    c.save()
    return response

