from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, DeliveryMan, Plant, ShoppingCart, CartItem, Wishlist, WishlistItem, Payment, Order, OrderItem, Review

# Register your models here.

# by TOH EE LIN
class CustomUserAdmin(UserAdmin):
    model = User
    # Add custom fields to list_display to show up in the admin list view.
    list_display = ('username', 'email', 'is_customer', 'is_deliveryman', 'is_admin', 'is_staff', 'is_active')
    # Add custom fields to fieldsets to include them in the admin form view.
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_customer', 'is_deliveryman', 'is_admin')}),
    )

# by TOH EE LIN
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'get_user_email', 'customer_state')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'   # Sets the column header

# by TOH EE LIN
class DelmanAdmin(admin.ModelAdmin):
    list_display = ('deliveryman_name', 'get_user_email', 'deliveryman_phone_number')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'  

# by TOH EE LIN
class PlantAdmin(admin.ModelAdmin):
    list_display = ('plant_name', 'plant_price', 'plant_availability')

# by TOH EE LIN
class CartAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email', 'cart_total_price')

    def get_customer_email(self, obj):
        return obj.customer.user.email
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.customer.customer_name
    get_customer_name.short_description = 'Customer Name'

# by TOH EE LIN
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email', 'get_plant','cart_plant_quantity', 'get_cartitem_price')

    def get_customer_email(self, obj):
        return obj.cart.customer.user.email 
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.cart.customer.customer_name
    get_customer_name.short_description = 'Customer Name'

    def get_plant(self, obj):
        return obj.plant.plant_name
    get_plant.short_description = 'Plant Name'

    def get_cartitem_price(self, obj):
        return obj.cart_item_price
    get_cartitem_price.short_description = 'Item Price (x Quantity)' 

# by TOH EE LIN
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email')

    def get_customer_email(self, obj):
        return obj.customer.user.email
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.customer.customer_name
    get_customer_name.short_description = 'Customer Name'

# by TOH EE LIN
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email', 'get_plant')

    def get_customer_email(self, obj):
        return obj.wishlist.customer.user.email
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.wishlist.customer.customer_name
    get_customer_name.short_description = 'Customer Name'

    def get_plant(self, obj):
        return obj.plant.plant_name
    get_plant.short_description = 'Plant Name'

# by TOH EE LIN
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email', 'payment_cost', 'receive_method')
    
    def get_customer_email(self, obj):
        return obj.customer.user.email
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.customer.customer_name
    get_customer_name.short_description = 'Customer Name'  

# by TOH EE LIN
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email', 'get_payment_cost', 'get_order_date', 'get_receivemethod', 'order_status', 'get_deliveryman_name')

    def get_customer_email(self, obj):
        return obj.customer.user.email
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.customer.customer_name
    get_customer_name.short_description = 'Customer Name'

    def get_payment_cost(self, obj):
        return obj.payment.payment_cost
    get_payment_cost.short_description = 'Payment Cost'

    def get_receivemethod(self, obj):
        return obj.payment.receive_method
    get_receivemethod.short_description = 'Receive Method' 

    def get_order_date(self, obj):
        return obj.payment.order_date
    get_order_date.short_description = 'Order Date' 

    def get_deliveryman_name(self, obj):
        try:
            return obj.delman.deliveryman_name
        except:
            return None
    get_deliveryman_name.short_description = 'Deliveryman Name' 

# by TOH EE LIN
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'get_customer_email', 'get_plant','plant_quantity', 'get_orderitem_price')

    def get_customer_email(self, obj):
        return obj.order.customer.user.email    # path: OrderItem -> Order -> Customer -> User
    get_customer_email.short_description = 'Email'  

    def get_customer_name(self, obj):
        return obj.order.customer.customer_name
    get_customer_name.short_description = 'Customer Name'

    def get_plant(self, obj):
        return obj.plant.plant_name
    get_plant.short_description = 'Plant Name'

    def get_orderitem_price(self, obj):
        return obj.order_item_price
    get_orderitem_price.short_description = 'Item Price (x Quantity)' 

# by TOH EE LIN
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_plant', 'rating', 'comment')
    
    def get_plant(self, obj):
        return obj.order_item.plant.plant_name
    get_plant.short_description = 'Plant Name' 
 
 # by TOH EE LIN
admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(DeliveryMan, DelmanAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(ShoppingCart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Review, ReviewAdmin)
