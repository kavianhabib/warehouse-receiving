from numpy import negative
import openpyxl
import pandas as pd
from pandas.core.algorithms import quantile
from .models import Product, Vendor, PurchaseOrder, PurchaseProduct
from .constants import EXCEL_STANDARD_HEADER ,VENDOR_EXCEL_STANDARD_HEADER , PO_EXCEL_STANDARD_HEADER
import xlsxwriter
from django.utils.dateparse import parse_date

def process_excel_file(file_name, update=True):
    file = (file_name)
    newData = pd.read_excel(file,converters={'ScannedCode':str,'UPC':str})
    
    columns_header = newData.columns
    check = all(item in columns_header for item in EXCEL_STANDARD_HEADER)

    if(not check):
        print("wrong excel format")
    else:
        rows , cols = newData.shape
#   'ScannedCode', 'ShelfLocation', 'Quantity', 'Description', 'UPC'

        created_set = []
        updated_set = []
        for i in range (rows):
            if not Product.objects.filter(id =newData["ScannedCode"][i]).exists():
                pro =Product.objects.create(name =newData["Description"][i], id = newData["ScannedCode"][i], count = newData["Quantity"][i], upc_code = str(newData["UPC"][i]), vendor = newData["vendor"][i] )
                pro.save()
                created_set.append(pro)
            else:
                if update:
                    pro, update = Product.objects.update_or_create(id = newData["ScannedCode"][i], defaults= {'name' :newData["Description"][i], 'count' : newData["Quantity"][i], 'upc_code' : str(newData["UPC"][i]), 'vendor' : newData["vendor"][i]} )
                    pro.save()      
                    updated_set.append(pro)
    
    return created_set,updated_set


def export_excel(session):
    print("exporting excel file")
    file_name = str(session.date)+"-"+str(session.id)+"-receiving.xlsx"
    smart_file = str(session.date)+"-"+str(session.id)+"-smart_input.xlsx"

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    smart_workbook = xlsxwriter.Workbook(smart_file)
    smart_worksheet = smart_workbook.add_worksheet()
    counter = 1
    smart_counter = 1

    smart_worksheet.write("A1", "ScannedCode")
    smart_worksheet.write("B1", "ShelfLocation")
    smart_worksheet.write("C1", "Quantity")
    smart_worksheet.write("D1", "Description")
    smart_worksheet.write("F1", "UPC")
    smart_counter += 1

    # sort producst based on vendor
    products = session.products.all().order_by('product__vendor')

    # styling for merged section
    merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow',
    'bg_color':'yellow'})
    worksheet.merge_range("A"+str(counter)+":"+"C"+str(counter), 'Merged Range', merge_format)
    pre_product = products[0]
    worksheet.write("A"+str(counter), pre_product.product.vendor)
    counter +=1

    for p in products:
        smart_worksheet.write("A"+str(smart_counter), p.product.id)
        smart_worksheet.write("B"+str(smart_counter), "")
        smart_worksheet.write("C"+str(smart_counter), p.quantity)
        smart_worksheet.write("D"+str(smart_counter), p.product.name)
        smart_worksheet.write("F"+str(smart_counter), p.product.upc_code)

        if(pre_product.product.vendor != p.product.vendor):
            counter +=1
            worksheet.merge_range("A"+str(counter)+":"+"C"+str(counter), 'Merged Range', merge_format)
            worksheet.write("A"+str(counter), p.product.vendor)
            counter +=1
        worksheet.write("A"+str(counter), p.product.vendor)
        worksheet.write("B"+str(counter), p.product.name)
        worksheet.write("C"+str(counter), p.quantity)

        counter +=1
        smart_counter += 1
        pre_product = p
        # session.products.remove(p)

    session.closed = True
    session.report_file = file_name
    session.save()
    workbook.close()
    smart_workbook.close()
    return file_name, smart_file


def process_vendor_excel_upload(file_name, update=True):
    file = (file_name)
    new_data = pd.read_excel(file,converters={'Phone #':str, 'Fax #':str})

    column_headers = new_data.columns
    check = all(item in column_headers for item in VENDOR_EXCEL_STANDARD_HEADER)

    if(not check):
        return False
    
    rows, cols = new_data.shape

    created_set = []
    updated_set = []

    for i in range(rows):
        print(new_data['Phone #'][i])
        if not Vendor.objects.filter(id = new_data['Vendor #'][i]).exists():
            vendor = Vendor.objects.create(id = new_data['Vendor #'][i], name = new_data['Name'][i],
            address = new_data['Address Line 1'][i], city = new_data['City'][i], state = new_data['State'][i],
            zip = new_data['Zip'][i], country = new_data['Country'][i], contact = new_data['Contact'][i],
            phone_number =new_data['Phone #'][i], email = new_data['Email'][i], 
            source =new_data['Source'][i] , fax_number = new_data['Fax #'][i])
            vendor.save()
            created_set.append(vendor)
        else:
            if update:
                vendor , update = Vendor.objects.update_or_create(id = new_data['Vendor #'][i], name = new_data['Name'][i],
            address = new_data['Address Line 1'][i], city = new_data['City'][i], state = new_data['State'][i],
            zip = new_data['Zip'][i], country = new_data['Country'][i], contact = new_data['Contact'][i],
            phone_number =new_data['Phone #'][i], email = new_data['Email'][i], 
            source =new_data['Source'][i] , fax_number = new_data['Fax #'][i])
                vendor.save()
                updated_set.append(vendor)
    
    return created_set, updated_set

def check_file(header, file_header):
    check = all(item in file_header for item in header)
    
    return check

def import_purchase_order(file_name,vendor_id):

    new_data = pd.read_excel(file_name, converters={'PO #':int, 'Box #':int, 'Pack':int,'On Hand':int,
     'Start Label #':int, 'End Label #':int,'Arrival Date':str })
    print(check_file(PO_EXCEL_STANDARD_HEADER, new_data.columns))
    if(check_file(PO_EXCEL_STANDARD_HEADER, new_data.columns)):
        
        rows, cols = new_data.shape
        po_number = new_data['PO #'][0]
        po= None
        vendor_name = ''
        if PurchaseOrder.objects.filter(po_number = po_number).exists():
            return True,0
        else:
            print(new_data['Arrival Date'][0][:10])
            dv_date = parse_date(new_data['Arrival Date'][0][:10])
            vendor = Vendor.objects.filter(id = vendor_id)[0]
            vendor_name = vendor.name
            po = PurchaseOrder.objects.create(delivery_date = dv_date, po_number = po_number, vendor = vendor)
            po.save()


        for i in range(rows):
            product_code = new_data['Product Code'][i]
            if Product.objects.filter(id = product_code).exists():
                product = Product.objects.get(id = product_code)
                purchase_product = PurchaseProduct.objects.create(product = product,
                quantity = new_data['End Label #'][i],pack =new_data['Pack'][i],
                measure_unit =   new_data['UoM'][i], box_number = new_data['Box #'][i])
                purchase_product.save()

                po.products.add(purchase_product)
                po.number_ordered = po.number_ordered + new_data['End Label #'][i]
                po.save()
            else:
                product = Product.objects.create(id =product_code, name = new_data['Description'][i],
                count = new_data['Pack'][i])
                product.save()

                purchase_product = PurchaseProduct.objects.create(product = product,
                quantity = new_data['End Label #'][i],pack =new_data['Pack'][i],
                measure_unit =   new_data['UoM'][i], box_number = new_data['Box #'][i])
                purchase_product.save()

                po.products.add(purchase_product)
                po.number_ordered = po.number_ordered + new_data['End Label #'][i]
                po.save()

        return po_number, vendor_name

    else:
        return False,0

    



    

