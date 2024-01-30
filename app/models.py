from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# by TOH EE LIN
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_deliveryman = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) 
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    # Remove 'email' from here since it's the USERNAME_FIELD

# by TOH EE LIN
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')

# by TOH EE LIN
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer_profile')
    customer_name = models.CharField(max_length=80, default='Unknown')
    customer_address = models.CharField(max_length=200)
    customer_state = models.CharField(max_length=30)
    customer_ic = models.CharField(max_length=30, unique=True)
    customer_phone_number = models.BigIntegerField()

    def __str__(self):
        return self.user.email    # Using the email field from the related User object

# by TOH EE LIN
class DeliveryMan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='deliveryman_profile')
    deliveryman_name = models.CharField(max_length=80, default='Unknown')
    deliveryman_address = models.CharField(max_length=200)
    deliveryman_state = models.CharField(max_length=30)
    deliveryman_ic = models.CharField(max_length=30, unique=True)
    deliveryman_phone_number = models.BigIntegerField()

    def __str__(self):
        return self.user.email

# by TOH EE LIN  
class Plant(models.Model):
    plant_name = models.CharField(max_length=80)
    plant_image = models.ImageField(upload_to='plant/')
    plant_description = models.CharField(max_length=500)
    plant_price = models.DecimalField(max_digits=5, decimal_places=2)
    plant_availability = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])

    def __str__(self):
        return self.plant_name

# by TOH EE LIN
class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shopping_carts')
    cart_total_price = models.DecimalField(max_digits=5, decimal_places=2)

# by TOH EE LIN
class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='cart_items')
    cart_plant_quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    cart_item_price = models.DecimalField(max_digits=5, decimal_places=2)


# by TOH EE LIN
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlists')

# by TOH EE LIN
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='wishlist_items')

# by TOH EE LIN
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    shipping_fee = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(99.99)])
    payment_cost = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(9999.99)])
    receive_method = models.CharField(max_length=10)
    order_date = models.DateField()
    order_total_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(9999.99)])

# by TOH EE LIN
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='orders')
    delman = models.ForeignKey(DeliveryMan, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_status = models.CharField(max_length=30)

# by TOH EE LIN
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='order_items')
    plant_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    order_item_price = models.DecimalField(max_digits=5, decimal_places=2)
    to_review = models.BooleanField(default=True)

# by TOH EE LIN
class Review(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=500)