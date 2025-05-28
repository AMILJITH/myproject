from django.urls import path
from myapp import views 
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import block_seller, unblock_seller
urlpatterns = [

    path('home/', views.home, name='home'),
    path('register_user/', views.register_user, name='register_user'),
    path('sellerregister/', views.register_seller, name='sellerregister'),
    path('', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('order/', views.order_form, name='order_form'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('add-quantity/<int:item_id>/', views.add_quantity, name='add_quantity'),
    path('subtract-quantity/<int:item_id>/', views.subtract_quantity, name='subtract_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), 
    path('orders/', views.view_orders, name='view_orders'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('search/', views.search_products, name='search_products'), path('seller/orders/', views.view_orders_for_seller, name='seller_orders'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
      path('sellers/', views.seller_list, name='seller_list'),
    path('users/',views.user_list, name='user_list'),path('adminbase/', views.adminbase, name='adminbase'),
        path('users/', views.user_list, name='user_list'),
    path('sellers/', views.seller_list, name='seller_list'), path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('block-seller/<int:seller_id>/', block_seller, name='block_seller'),
    path('unblock-seller/<int:seller_id>/', unblock_seller, name='unblock_seller'),


  



    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




