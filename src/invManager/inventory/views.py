from io import SEEK_CUR
from django import forms, template
from django.db import models
from django.forms.widgets import DateInput
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from numpy.core.fromnumeric import prod
from pandas.core.algorithms import isin
from inventory.models import Product, Session,SessionItem, PurchaseOrder, Vendor, PurchaseProduct
from .forms import ProductForm, VendorForm, UploadFileForm,CreatePurchaseOrderForm,DateForm
from django.http import HttpResponseRedirect
from .processor import process_excel_file, export_excel, process_vendor_excel_upload,import_purchase_order
from django.http import HttpResponse, Http404
from django.views.generic import View, DetailView, ListView 
from django.contrib import messages
from django.utils.dateparse import parse_date
import os
# Create your views here.

def get_clone(products):
    copy = []
    for p in products:
        copy.append(p)

    return copy




def index_view(request):
    return render(request, "index.html", {})
    
def download(request,id, file_name):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_name)
            return response
    raise Http404

def warehouse_summary_view(request, id):
    session = get_object_or_404(Session, id = id)
    file_name = ""
    smart_file = ""
    report_file = None
    smart_file = None
    if request.method == 'POST':
        file_name, smart_file = export_excel(session)
    context= {
        "products" : session.products.all(),
        "file_name": file_name,
        "smart_file" : smart_file,
        "session" : session
      
    }
    return render(request, "warehouse_summary.html",context)

def decrease_quantity(request,id, product_id):
    session = get_object_or_404(Session, id = id)
    product = session.products.get(id = product_id)
    product.quantity -=1
    product.save()
    return redirect("..")

def increase_quantity(request, id, product_id):
    session = get_object_or_404(Session, id = id)
    product = session.products.get(id = product_id)
    product.quantity +=1
    product.save()
    return redirect("..")

def warehouse_receiving_view(request, id):
    session = get_object_or_404(Session, id = id)
    create_promp = False
    if request.method == "POST":
        try:
            if(session.products.filter(product__upc_code = request.POST["search"]).exists()):
                sessionItem = session.products.filter(product__upc_code = request.POST["search"])[0]
                sessionItem.quantity +=1
                sessionItem.save()
            else:
                sessionItem = SessionItem.objects.create(product = Product.objects.get(upc_code = request.POST["search"]))
                sessionItem.save()
                session.products.add(sessionItem)
                session.item_count +=1
                session.save()
        except:
            create_promp = True
        # if session.objects.filter()
        # try:

        #     product = Product.objects.get(upc_code = request.POST["search"])
        #     product.count =  product.count + 1
        #     product.save()
        
        #     session.products.add(product)
        #     session.save()
        # except:
        #     create_promp = True


    # elif request.method == "DELETE":
    #         # products.append(request.POST["search"])
    #     print("it is deleting")
    if request.method == "GET":
        print("this is get")
    queryset =  session.products.all()
    context = {
        "products" : queryset,
        "session" : session,
        "create_promp" : create_promp,
    }
    return render(request, "warehouse_receiving.html",context)

def start_session_view(request):
    print("in the session")
    session = None
    if request.method == "POST":
        if (Session.objects.filter(closed = False).exists()):
            session = Session.objects.filter(closed = False)[0]
        else:
            session = Session.objects.create( item_count = 0, closed = False)
            session.save()
        return redirect("/warehouse_receiving/"+ str(session.id))

    context = {
        "session" : session
    }
    return render(request, "new_session.html", context)

def warehouse_delete_view(request,id):
    global session, products
    if request.method == "POST":
        print(id)
        # products.remove(id)
        # return redirect("warehouse_receiving/")
   
    context = {
        # "products":products
    }
    return render(request, "warehouse_delete.html",context)
def product_add_view(request, condition, id = 0):
    form = ProductForm(request.POST or None) 
    if(request.method == "POST"):
        if form.is_valid() and condition == 0:
            form.save()
            form = ProductForm()
        elif form.is_valid() and condition == 1:
            form.save()
            form = ProductForm()
            return redirect("..")

    
    context = {
        "form":form
    }
    return render(request, "product_add.html",context)

def vender_add_view(request):
    form = VendorForm(request.POST or None)  
    if form.is_valid():
        form.save()

    context = {
        "form":form
    }
    return render(request, "vendor_add.html",context)

# def bulk_add_view(request):
#     context = {
#         # "form":form
#     }
#     return render(request, "bulk_add.html",context)

def upload_file(request):
    created_set = None
    updated_set = None
    form = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            created_set, updated_set = process_excel_file(request.FILES['file'])
            context = {
                'created_set' : created_set,
                'updated_set' : updated_set
            }
            return render(request, 'view_uploaded_data.html', context)
             # return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    context = {
        'form' : form,
        'created_set' : created_set,
        'updated_set' : updated_set

    }
    return render(request, 'bulk_add.html', context)

def delete_product_view(request,id, product_id):
    session = get_object_or_404(Session, id = id)
    product = session.products.filter(id =product_id)[0]
    if request.method == "POST":
        session.products.remove(product)
        SessionItem.objects.filter(id = product_id).delete()
 
        #  or we can delete using
        # instance = SessionItem.objects.get(id = product_id)
        # instance.delete()
        return redirect("..")
    queryset =  session.products.all()
    context = {
        "product":product,
        "products" : queryset,
        "session" : session
    }
    
    # return render(request, 'confirm_deletion.html', context)
    return render(request, "warehouse_receiving.html",context)


    # revers foreign relationship
    # Category.objects.get(id = 1).item_set.all()

    # return categories instead of items
    # Categories.objects.all()
    # for item in category.item_set.all()
    # do whatever with item
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from barcode import EAN13
from .pdf_generator import make_pdf_file, make_pdf_pos_by_date


def create_barcode(code):
    my_code = EAN13(code)
    my_code.save(str(code))


def html_to_pdf(template_src, context_dict = {}):
    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result, default_css = open('inventory/static/default_css.css','r').read())
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None

class ViewPDF(View):
    def get(self, *args, **kwargs):
        id = kwargs['po_number']
        po = PurchaseOrder.objects.filter(po_number = id)
        if po.exists():
            pdf= make_pdf_file(po[0])
            return HttpResponse(pdf, content_type = 'application/pdf')
        else:
            messages.error(self.request, 'There is no such purchase order to print.')
            return render(self.request, 'view_purchase_orders.html')


class DownloadPDF(View):
    def get(self, *args, **kwargs):  
        queryset = {}
        pdf = html_to_pdf('label_template', queryset)  

        response = HttpResponse(pdf, content_type = 'application/pdf')
        filename = "labels_%s.pdf" %("1234")
        content = "attachment; filename='%s" %(filename)
        response['Content-Disposition'] = content
        return response

class PrintPurchaseOrderLabelByDate(View):
    def get(self, *args, **kwargs):
        pos = PurchaseOrder.objects.filter(delivery_date = parse_date(kwargs['date']))
        if pos.exists():
            pdf = make_pdf_pos_by_date(pos)
            return HttpResponse(pdf, content_type = 'application/pdf')
        else:
            messages.error(self.request, 'There is no such purchase order to print.')
            return render(self.request, 'view_purchase_orders.html')


class PurchaseOrderView(View):
    def get(self, *args,**kwargs):
        return render(self.request, 'purchase_order.html')

class PurchaseOrderListView(View):
    date = DateForm()
    def get(self, *args, **kwargs):
        
        context = {
            'date': self.date,
            'purchaseOrder': None
        }
        return render(self.request, 'view_purchase_orders.html', context)

    def post(self, *args, **kwargs):
        date = parse_date(self.request.POST['date'])
        qs = PurchaseOrder.objects.filter(delivery_date = date)
        if qs.exists():
            return render(self.request, 'view_purchase_orders.html', {'date':self.date, 'purchaseOrder': qs, 'selected_date':self.request.POST['date']})
        else:
            messages.error(self.request, "There is no purchase order for given date.")
            return render(self.request, 'view_purchase_orders.html', {'date':self.date, 'purchaseOrder':None})

class CreatePurchaseOrderView(View):
    vendors = Vendor.objects.all()
    form = CreatePurchaseOrderForm()
    upload_form = UploadFileForm()
    def get(self, *args, **kwargs):
    
        upload_form = UploadFileForm()
        context = {
            'form':self.form,
            'vendors': self.vendors,
            'upload_form': upload_form,
        }
        return render(self.request, 'create_purchase_order.html', context)
    def post(self, *args, **kwargs):
        po_num, vendor_name=import_purchase_order(self.request.FILES['file'],self.request.POST['vendor'] )
        if isinstance(po_num, bool) and po_num == False:
            messages.error(self.request, "Wrong purchase order file format!")
            return render(self.request, 'create_purchase_order.html',{'upload_form': self.upload_form, 'vendors': self.vendors})
        elif isinstance(po_num, bool) and po_num == True:
            messages.error(self.request, "Purchase order already in the system.")
            return render(self.request, 'create_purchase_order.html',{'upload_form': self.upload_form, 'vendors': self.vendors})       
        else:
            po = PurchaseOrder.objects.get(po_number = po_num)
            form = CreatePurchaseOrderForm()
            po_products = po.products.all()
            return render(self.request, 'create_purchase_order.html',{'upload_form': self.upload_form, 'vendors': self.vendors, 'products': po_products,
            'vendor_name': vendor_name})


    
# class CreatePurchaseOrderListView(ListView):
#     model = Vendor
#     template_name = 'create_purchase_order.html'

#     def get(self, request):
#         form = CreatePurchaseOrderForm()
#         print("this is inside the get")
#         return render(self.request, self.template_name, {'form':form})



def upload_file(request):
    created_set = None
    updated_set = None
    form = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            created_set, updated_set = process_excel_file(request.FILES['file'])
            context = {
                'created_set' : created_set,
                'updated_set' : updated_set
            }
            return render(request, 'view_uploaded_data.html', context)
             # return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    context = {
        'form' : form,
        'created_set' : created_set,
        'updated_set' : updated_set

    }
    return render(request, 'bulk_add.html', context)


def populate_vendor(request):
    created_set = None
    update_set = None
    form = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            created_set, update_set = process_vendor_excel_upload(request.FILES['file'])
            context = {
                'created_set' : created_set,
                'updated_set' : update_set
            }
            # return render(request, 'view_uploaded_vendor_data.html', context)
    else:
        form = UploadFileForm()
    context = {
        'form' : form,
        'created_set' : created_set,
        'updated_set' : update_set
    }

    return render(request, 'populate_vendor.html', context)

class PurchaseOrderReceivingView(View):
    date = None
    qs = None
    def get(self, *args,**kwargs):
        self.date = parse_date(kwargs['date'])
        self.qs = PurchaseOrder.objects.filter(delivery_date = self.date)
        if self.qs.exists():
            context = {
                'purchaseOrder' : self.qs,
                'selected_date' : self.date
            }
            return render(self.request, 'receiving_po_products.html', context)
        else:
            messages.error(self.request, "There are no purchase order for the selected date.")
            return render(self.request,'view_purchase_orders.html')
        
    def post(self, *args, **kwargs):
        
        barcode = self.request.POST['search']
        products = PurchaseProduct.objects.filter(barcode = barcode)
        self.date = parse_date(kwargs['date'])
        self.qs = PurchaseOrder.objects.filter(delivery_date = self.date)
        context = {
                'purchaseOrder' : self.qs,
                'selected_date' : self.date
            }
        if products.exists():
            product = products[0]
            if product.received_quantity <= product.quantity:
                product.received_quantity = product.received_quantity+1
                product.save()
                print(product.received_quantity)
            else:
                print('inside here')
                product.received_quantity += 1
                messages.error(self.request, "There is more product received than ordered.")
            products[0].save()
            po = products[0].purchaseorder_set.all()[0]
            po.number_received +=1
            if po.number_received >= po.number_ordered/2:
                po.badge = 'W'
            if po.number_received == po.number_ordered:
                po.badge = 'S'
            po.save()
        else:
            messages.error(self.request, "There is no such product in purchase order, please, check the code.")
            return render(self.request, 'receiving_po_products.html', context)
        if self.qs.exists():
            # context = {
            #     'purchaseOrder' : self.qs,
            #     'selected_date' : self.date
            # }
            return render(self.request, 'receiving_po_products.html', context)
        else:
            messages.error(self.request, "There are no purchase order for the selected date.")
            return render(self.request,'view_purchase_orders.html')
class SinglePurchaseOrderView(View):

    def get(self, *args, **kwargs):
        po_number = kwargs['po_number']
        po = PurchaseOrder.objects.filter(po_number = po_number)
        # print(po)
        # products = po.products.all()
        # print(products)
        if po.exists():
            p = po[0]
            context = {
                'purchaseOrder': p.products.all(),
                'po':p
            }
            return render(self.request, 'view_single_purchase_order.html', context)
        
        return render(self.request, 'view_single_purchase_order.html', {})
    def post(self, *args, **kwargs):
        quantity = self.request.POST['quantity']
        product_id = self.request.POST['product_id']
        po_number = kwargs['po_number']

        product= PurchaseProduct.objects.filter(id = product_id)[0]
        product.received_quantity = quantity
        product.save()

        po = PurchaseOrder.objects.filter(po_number = po_number)
        if po.exists():
            p = po[0]
            context = {
                'purchaseOrder': p.products.all(),
                'po':p
            }
            return render(self.request, 'view_single_purchase_order.html', context)

       

def update_purchase_product_quantity(request, id):
    purchase_product = get_object_or_404(PurchaseProduct, id = id)
    # print(request.POST)
    # return render(request, 'view_single_purchase_order.html', {})

def increase_purchase_product_quantity(request, id):
    purchase_product = get_object_or_404(PurchaseProduct, id = id)
    purchase_product.received_quantity +=1
    purchase_product.save()

    po = purchase_product.purchaseorder_set.all()
    if po.exists():
        p = po[0]
        context = {
            'purchaseOrder': p.products.all(),
            'po':p
        }
        return render(request, 'view_single_purchase_order.html', context)

def decrease_purchase_product_quantity(request, id):
    purchase_product = get_object_or_404(PurchaseProduct, id = id)
    if purchase_product.received_quantity >= 1:
        purchase_product.received_quantity -=1
        purchase_product.save()
    else:
        messages.error(request, "Can not decrease lower than 0")

    po = purchase_product.purchaseorder_set.all()
    if po.exists():
        p = po[0]
        context = {
            'purchaseOrder': p.products.all(),
            'po':p
        }
        return render(request, 'view_single_purchase_order.html', context)

def delete_purchase_product(request, id):
    purchase_product = get_object_or_404(PurchaseProduct, id = id)
    po = purchase_product.purchaseorder_set.all()[0]

    po.products.remove(purchase_product)
    purchase_product.delete()
    po.save()
   
    context = {
        'purchaseOrder': po.products.all(),
        'po':po
    }
    return render(request, 'view_single_purchase_order.html', context)

def delete_purchase_order(request, po_number):
    if request.method == 'POST':
        po = get_object_or_404(PurchaseOrder, po_number=po_number)
        date = po.delivery_date
        
        for product in po.products.all():
            product.delete()
        po.delete()
        qs = PurchaseOrder.objects.filter(delivery_date = date)
        context = {
        'purchaseOrder' : qs,
        'selected_date' : date
        }
        return render(request, 'view_purchase_orders.html', context)

