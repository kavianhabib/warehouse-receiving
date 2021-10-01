from django.contrib import admin

# Register your models here.

from inventory.models import Session, SessionItem,Product,Vendor, PurchaseOrder, PurchaseProduct

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Session)
admin.site.register(SessionItem)
admin.site.register(PurchaseProduct)
admin.site.register(PurchaseOrder)