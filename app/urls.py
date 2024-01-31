from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("user/login/", views.loginPage, name="loginPage"),
    path("logout/", views.logout, name="logout"),
    path("adm/dashboard/", views.adminDashboard, name="adminDashboard"),
    path("adm/plant/manage/", views.plantManagement, name="plantManagement"),
    path("adm/plant/create", views.createPlant, name="createPlant"),
    path("adm/plant/update/<int:plant_id>/", views.updatePlant, name="updatePlant"),
    path("adm/plant/delete/<int:plant_id>/", views.deletePlant, name="deletePlant"),
    path("adm/order/", views.orderManagement, name="orderManagement"),
    path('adm/order/update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path("adm/delivery/", views.deliveryManagement, name="deliveryManagement"),
    path('adm/delivery/assign_delman/<int:order_id>/', views.assign_delivery, name='assign_delivery'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('plant_list/', views.plant_list_view, name='plant_list'),
    path('add_to_cart/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('add_to_wishlist/<int:plant_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('to_review/', views.to_review, name='to_review'),
    path('submit_review/<int:order_item_id>/', views.submit_review, name='submit_review'),
    path('checkout/', views.checkout, name='checkout'),
    path('delivery_details/', views.delivery_details, name='delivery_details'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('profile/edit/', views.update_profile, name='edit_profile'),  # For displaying the form
    path('profile/update/', views.update_profile, name='update_profile'),  # For handling the form submission
    #path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
]

# Add the following to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

