from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from .views import (warehouse_receiving_view, index_view, warehouse_delete_view,
 product_add_view,vender_add_view,upload_file,start_session_view,  warehouse_summary_view,
  download,delete_product_view, decrease_quantity, increase_quantity,PurchaseOrderView,CreatePurchaseOrderView,
  populate_vendor,ViewPDF,PurchaseOrderListView,PrintPurchaseOrderLabelByDate,PurchaseOrderReceivingView,
  SinglePurchaseOrderView,increase_purchase_product_quantity,decrease_purchase_product_quantity,
  delete_purchase_product,delete_purchase_order)

app_name = "inventory"

urlpatterns =[
    path('', index_view, name = "inventory_home"),
    path('warehouse_receiving/<int:id>/', warehouse_receiving_view, name = "inventory_receiving"),
    path('warehouse_receiving/<int:id>/product_add/<int:condition>', product_add_view, name = "product_add_session"),
    path('warehouse_receiving/<int:id>/end_session', warehouse_summary_view, name = "inventory_receiving"),
    path('warehouse_receiving/<int:id>/<str:product_id>/delete',delete_product_view, name = "delete"),
    path('warehouse_receiving/<int:id>/increase/<str:product_id>',increase_quantity, name = "increase"),
    path('warehouse_receiving/<int:id>/decrease/<str:product_id>',decrease_quantity, name = "decrease"),
    path('warehouse_receiving/<int:id>/end_session/download/<str:file_name>',download, name = "download"),
    # url(r'^download/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    path('warehouse_receiving/<int:id>/delete', warehouse_delete_view, name = "inventory_receiving_delete"),
    path('product_add/<int:condition>', product_add_view, name = "product_add"),
    path('vendor_add/', vender_add_view, name = "vendor_add"),
    path('upload_file/', upload_file, name = "upload_add"),
    path('new_session/', start_session_view, name = "new_session"),
    path('purchase-order/', PurchaseOrderView.as_view(), name = "purchase-order"),
    path('create-purchase-order/', CreatePurchaseOrderView.as_view(), name = "create-purchase-order"),
    path('view-purchase-orders/', PurchaseOrderView.as_view(), name = "view-purchase-orders"),
    path('populate_vendor/', populate_vendor, name = "populate-vendor"),
    path('purchase-orders-list/', PurchaseOrderListView.as_view(), name = "purchase-orders-list"),
    path('view-pdf/<int:po_number>', ViewPDF.as_view(), name = "view-pdf"),
    path('print-purchase-order-by-date/<str:date>', PrintPurchaseOrderLabelByDate.as_view(), name = "print-purchase-order-by-date"),
    path('receive-purchase-order-product/<str:date>', PurchaseOrderReceivingView.as_view(), name = "receive-purchase-order-product"),
    path('view-purchase-order/<int:po_number>', SinglePurchaseOrderView.as_view(), name = 'view-purchase-order'),
    path('update-purchase-product-quantity/<int:id>', SinglePurchaseOrderView.as_view(), name = 'update-purchase-product-quantity'),
    path('increase_purchase_product_quantity/<int:id>', increase_purchase_product_quantity, name = 'increase_purchase_product_quantity'),
    path('decrease-purchase-product-quantity/<int:id>', decrease_purchase_product_quantity, name = 'decrease-purchase-product-quantity'),
    path('delete-purchase-product/<int:id>', delete_purchase_product, name = 'delete-purchase-product'),
    path('delete-purchase-order/<int:po_number>', delete_purchase_order, name = 'delete-purchase-order'),

# increase_purchase_product_quantity
# update-purchase-product-quantity
# view-purchase-order
    # receive-purchase-order-product
#     create-purchase-order'
# 'view-purchase-orders'

]

