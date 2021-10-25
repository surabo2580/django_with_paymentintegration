from . import views
from django.urls import path


urlpatterns = [
    path('',views.shopHome,name='shophome'),
    path('tracker/',views.tracker,name='tracker'),
    path('search/',views.search,name='search'),
    path('productview/<int:product_id>',views.productView,name='productview'),
    path('checkout/',views.checkOut,name='checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest'),




]
