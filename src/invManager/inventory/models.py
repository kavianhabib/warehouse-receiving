from django.db import models
from numpy import mod

from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse

# Create your models here.

BADGE_CHOICES =(
    ('S','success'),
    ('D','danger'),
    ('W','warning'),
)

   
class Product(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=100)
    upc_code = models.CharField(max_length=20, null = True,unique=True)
    count = models.IntegerField()
  
    def __str__(self):
        return self.name


    def update(self,id, name, upc_code, count,vendor):
        self.id = id
        self.name = name
        self.upc_code = upc_code
        self.count = count
        self.vendor =vendor

class Vendor(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, null = True)
    state = models.CharField(max_length=3, null = True)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    contact = models.CharField(max_length=100, null = True)
    phone_number = models.CharField(max_length=20, null = True)#PhoneNumberField()
    email = models.EmailField(max_length=100,null = True)
    products = models.ManyToManyField(Product)
    fax_number = models.CharField(max_length=20, null = True)#PhoneNumberField(blank=True)
    source = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.name

class PurchaseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    received_quantity = models.IntegerField(default=0)
    pack = models.IntegerField()
    measure_unit = models.CharField(max_length=100)
    box_number = models.IntegerField()
    barcode = models.CharField(max_length=100, null = True)
    # barcode = models.CharField(max_length=100, null = True)

    def get_update_quantity_url(self):
        return reverse('inventory:update-purchase-product-quantity', kwargs ={
            'id':self.id
        })

    def get_increase_quantity_url(self):
        return reverse('inventory:increase_purchase_product_quantity', kwargs ={
            'id':self.id
        })
    def get_decrease_quantity_url(self):
        return reverse('inventory:decrease-purchase-product-quantity', kwargs ={
            'id':self.id
        })   
    def get_delete_url(self):
        return reverse('inventory:delete-purchase-product', kwargs ={
            'id': self.id
        }) 
    
class PurchaseOrder(models.Model):
    creation_date = models.DateField(auto_now=True)
    delivery_date = models.DateField()
    po_number = models.IntegerField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    products = models.ManyToManyField(PurchaseProduct)
    number_ordered = models.IntegerField(null = True, default=0)
    number_received = models.IntegerField(null = True, default=0)
    badge = models.CharField(choices=BADGE_CHOICES, max_length=1, default='D')

    def get_label_url(self):
        return reverse("inventory:view-pdf", kwargs = {
            'po_number':self.po_number
        })
    def get_purchase_order_view_url(self):
        return reverse('inventory:view-purchase-order', kwargs={
            'po_number':self.po_number
        })
    def get_purchase_order_delete_url(self):
        return reverse('inventory:delete-purchase-order', kwargs={
            'po_number':self.po_number
        })


class SessionItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)


class Session(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=True)
    item_count = models.IntegerField()
    closed = models.BooleanField()
    report_file = models.FileField(null = True)
    products = models.ManyToManyField(SessionItem)

    def get_absolute_url(self):
        return f"../warehouse_receiving/{self.id}"

