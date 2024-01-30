from django.db.models import Sum, Q
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
#from .models import DeliveryMan, Plant, Order, Review
from .models import DeliveryMan, Plant, Order, Review,ShoppingCart,CartItem,Customer,WishlistItem,Wishlist,OrderItem,Payment
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def home(request):
    return render(request, "index.html")

# by TEO YU JIE
def loginPage(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        user = authenticate(request, email=user_email, password=user_password)
        if user is not None:
            login(request, user)
            # Redirect to different dashboards based on the user's role
            if user.is_admin:
                return redirect('adminDashboard')  
            # elif user.is_deliveryman:
            #     return redirect('deliveryman_dashboard_url')  # Replace with deliveryman de URL 
            elif user.is_customer:
                return redirect('customer_dashboard')  # Replace with with customer de URL   
        else:
            # Authentication failed
            isError = True
            return render(request, 'login.html', {"isError": isError})
    else:
        return render(request, 'login.html', {"isError": False})

# by TOH EE LIN  
@user_passes_test(lambda user: user.is_admin)
def adminDashboard(request):
    return render(request, "admin_dashboard.html")

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def plantManagement(request):
    search_query = request.GET.get('search_query', '')   # Get search query from GET parameters, default to empty string

    if search_query:
        plants = Plant.objects.filter(plant_name__icontains=search_query)
    else:
        plants = Plant.objects.all()
    
    # Iterate over each plant and retrieve associated reviews
    for plant in plants:
        plant.reviews = Review.objects.filter(order_item__plant=plant)

    return render(request, "plant_management.html", {"plants": plants, "search_query": search_query}) 

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def createPlant(request):
    if request.method == 'POST':
        # Get the data from the form
        plant_name = request.POST.get('plant_name')
        plant_description = request.POST.get('plant_description')
        plant_price = request.POST.get('plant_price')
        plant_availability = request.POST.get('plant_availability')
        plant_image = request.FILES.get('plant_image')

        # Create a new Plant instance and save it
        Plant.objects.create(
            plant_name=plant_name,
            plant_description=plant_description,
            plant_price=plant_price,
            plant_availability=plant_availability,
            plant_image=plant_image
        )

        return redirect('plantManagement')

    # If not a POST request, just render the create plant form
    return render(request, "create_plant.html")

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def updatePlant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name')
        plant_description = request.POST.get('plant_description')
        plant_price = request.POST.get('plant_price')
        plant_availability = request.POST.get('plant_availability')
        plant_image = request.FILES.get('plant_image') if 'plant_image' in request.FILES else None

        plant.plant_name = plant_name
        plant.plant_description = plant_description
        plant.plant_price = plant_price
        plant.plant_availability = plant_availability
    
        if plant_image:
            plant.plant_image = plant_image
        plant.save()

        return redirect('plantManagement')
    else:
        # If not a POST request, pre-populate the form with plant data
        return render(request, "update_plant.html", {"plant": plant})

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def deletePlant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)   # This ensures the plant exists, or returns a 404 error
    plant.delete()
    messages.add_message(request, messages.SUCCESS, 'The plant has been deleted.') 
    return redirect('plantManagement')

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def orderManagement(request):
    search_query = request.GET.get('search_query', '')
    error_message = None

    orders = (
        Order.objects
        .select_related('customer')
        .prefetch_related('order_items')
        .annotate(total_plant_quantity=Sum('order_items__plant_quantity'))
        .exclude(
            Q(payment__receive_method='Pickup', order_status='Completed') |
            Q(payment__receive_method='Delivery', order_status='Ready')
        )
    )

    if search_query:
        try:
            search_query = int(search_query)

            orders = orders.filter(id=search_query)

            if not orders.exists():
                error_message = "No ongoing orders matched the entered order ID."

        except ValueError:
            error_message = "Invalid input. Please enter a numeric order ID."
            orders = Order.objects.none() 

    return render(request, "order_management.html", {"orders": orders, "search_query": search_query, "error_message": error_message})

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.order_status = request.POST.get('status')
        order.save()
        return redirect('orderManagement')  

    return redirect('orderManagement')

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def deliveryManagement(request):
    search_query = request.GET.get('search_query', '')
    error_message = None

    delivery_orders = (
        Order.objects
        .filter(payment__receive_method='Delivery', delman__isnull=True)
        .exclude(order_status='Completed')
        .select_related('customer', 'payment')
        .prefetch_related('order_items')
    )

    deliverymen = DeliveryMan.objects.all()

    if search_query:
        try:
            search_query = int(search_query)

            delivery_orders = delivery_orders.filter(id=search_query)

            if not delivery_orders.exists():
                error_message = "No ongoing orders matched the entered order ID."

        except ValueError:
            error_message = "Invalid input. Please enter a numeric order ID."
            delivery_orders = Order.objects.none()  

    return render(request, 'delivery_management.html', {'delivery_orders': delivery_orders, 'deliverymen': deliverymen, 'error_message': error_message})

# by TOH EE LIN
@user_passes_test(lambda user: user.is_admin)
def assign_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        deliveryman_id = request.POST.get('deliveryman')
        deliveryman = get_object_or_404(DeliveryMan, user_id=deliveryman_id)
        
        order.delman = deliveryman
        order.save()
        return redirect('deliveryManagement')
    
    return redirect('deliveryManagement')

def logout(request):
    django_logout(request)
    return redirect(home)

def customer_dashboard(request): 
    plant_objects = Plant.objects.all()
    for plant in plant_objects:
        plant.reviews = Review.objects.filter(order_item__plant=plant)

    item_name = request.GET.get('item_name')
    if item_name:
        plant_objects = plant_objects.filter(plant_name__icontains=item_name)
        if not plant_objects:
            message = "No matching plants found."
            return render(request, 'customer_dashboard.html', {'message': message})

    return render(request, 'customer_dashboard.html', {'plant_objects': plant_objects})

def plant_list_view(request):
    plant_objects = Plant.objects.all()
    for plant in plant_objects:
        plant.reviews = Review.objects.filter(order_item__plant=plant)

    item_name = request.GET.get('item_name')
    if item_name:
        plant_objects = plant_objects.filter(plant_name__icontains=item_name)
        if not plant_objects:
            message = "No matching plants found."
            context = {'message': message}
            return render(request, 'plant_list.html', context)

    context = {'plant_objects': plant_objects}
    return render(request, 'plant_list.html', context)

@login_required
def add_to_cart(request, plant_id):
    # Default the quantity to 1
    quantity = 1
    plant = get_object_or_404(Plant, id=plant_id)
    customer = request.user.customer_profile
    cart, created = ShoppingCart.objects.get_or_create(customer=customer, defaults={'cart_total_price': 0})
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        plant=plant,
        defaults={'cart_plant_quantity': quantity, 'cart_item_price': plant.plant_price}
    )
    if not created:
        # If the item is already in the cart, don't change the quantity
        pass
    return redirect('view_cart')


@login_required
def view_cart(request):
    customer = request.user.customer_profile
    total_price = 0
    try:
        cart = ShoppingCart.objects.get(customer=customer)
        items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.plant.plant_price * item.cart_plant_quantity for item in items)
    except ShoppingCart.DoesNotExist:
        items = []
    return render(request, 'cart.html', {'cart_items': items, 'total_price': total_price})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('view_cart'))

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.cart_plant_quantity = quantity
            item.save()
        else:
            item.delete()  # If the quantity is 0, remove the item
    return HttpResponseRedirect(reverse('view_cart'))

@login_required
def view_wishlist(request):
    customer = request.user.customer_profile
    wishlist_items = WishlistItem.objects.filter(wishlist__customer=customer)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    customer = request.user.customer_profile
    wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    WishlistItem.objects.get_or_create(wishlist=wishlist, plant=plant)
    return redirect('view_wishlist')

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id)
    if item.wishlist.customer == request.user.customer_profile:
        item.delete()
    return redirect('view_wishlist')

@login_required
def to_review(request):
    customer = request.user.customer_profile
    order_items_to_review = OrderItem.objects.filter(
        order__customer=customer,
        to_review=True
    )
    return render(request, 'to_review.html', {'order_items_to_review': order_items_to_review})

@login_required
def submit_review(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id, to_review=True)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating:
            Review.objects.create(
                order_item=order_item,
                rating=rating,
                comment=comment
            )
            order_item.to_review = False
            order_item.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('to_review')
        else:
            messages.error(request, 'Rating is required.')
    return render(request, 'submit_review.html', {'order_item': order_item})

@login_required
def checkout(request):
    customer = request.user.customer_profile
    cart = ShoppingCart.objects.get(customer=customer)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.plant.plant_price * item.cart_plant_quantity for item in items)
    
    if request.method == 'POST':
        receive_method = request.POST.get('receive_method')
        request.session['receive_method'] = receive_method  # Save the choice in the session
        if receive_method == 'pickup':
            return redirect('make_payment')
        elif receive_method == 'delivery':
            return redirect('delivery_details')
    
    # Pass the pickup and delivery options to the template
    context = {
        'cart_items': items,
        'total_price': total_price,
        'customer': customer
    }
    return render(request, 'checkout.html', context)


@login_required
def delivery_details(request):
    customer = request.user.customer_profile
    
    # Set shipping fee based on the customer's state
    if customer.customer_state in ['Sabah', 'Sarawak']:
        shipping_fee = Decimal('12.00')
    else:
        shipping_fee = Decimal('7.00')
    
    cart = ShoppingCart.objects.get(customer=customer)
    items = CartItem.objects.filter(cart=cart)
    plant_price = sum(item.plant.plant_price * item.cart_plant_quantity for item in items)
    total_price = plant_price + shipping_fee
    
    if request.method == 'POST':
        # Handle the order creation and payment process here
        # ...
        return redirect('make_payment')
    
    context = {
        'customer_name': customer.customer_name,
        'delivery_address': customer.customer_address,
        'plant_price': plant_price,
        'shipping_fee': shipping_fee,
        'total_price': total_price,
    }
    return render(request, 'delivery_details.html', context)

@login_required
def make_payment(request):
    customer = request.user.customer_profile
    cart = ShoppingCart.objects.get(customer=customer)
    items = CartItem.objects.filter(cart=cart)
    
    # Calculate the total cost of the plants in the cart
    plant_price = sum(item.plant.plant_price * item.cart_plant_quantity for item in items)
    
    # Retrieve the receive_method from the session
    receive_method = request.session.get('receive_method', 'pickup')
    shipping_fee = Decimal('0.00')
    
    # Calculate shipping fee based on the receive_method and the customer's state
    if receive_method == 'delivery':
        if customer.customer_state in ['Sabah', 'Sarawak']:
            shipping_fee = Decimal('12.00')
        else:
            shipping_fee = Decimal('7.00')
    
    # The total cost includes the shipping fee if applicable
    total_cost = plant_price + shipping_fee

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Create a Payment instance using your model's fields
        payment = Payment.objects.create(
            customer=customer,
            shipping_fee=shipping_fee,
            payment_cost=plant_price,  # Assuming this is the cost without shipping
            receive_method=receive_method,
            order_date=timezone.now().date(),  # Sets the order date to current date
            order_total_price=total_cost,  # Total cost including shipping
        )
        
        # Create an Order instance and link the Payment instance
        with transaction.atomic():
            new_order = Order.objects.create(
                customer=customer, 
                payment=payment,
                order_status='Processing'  # Or any other status you wish to start with
            )
            for item in items:
                OrderItem.objects.create(
                    order=new_order,
                    plant=item.plant,
                    plant_quantity=item.cart_plant_quantity,
                    order_item_price=item.plant.plant_price
                )
            cart.delete()  # Clear the shopping cart

        messages.success(request, 'Your payment has been successfully processed. Your order ID is {}'.format(new_order.id))
        return redirect('plant_list')

    # Include the necessary data in the context for rendering
    context = {
        'total_cost': total_cost,
        'plant_price': plant_price,
        'shipping_fee': shipping_fee,
        'receive_method': receive_method.title()  # Assuming you want to display "Pickup" or "Delivery" in the template
    }
    return render(request, 'make_payment.html', context)

@login_required
def my_orders(request):
    customer = request.user.customer_profile
    orders = Order.objects.filter(customer=customer).prefetch_related('order_items', 'payment')
    context = {'orders': orders}
    return render(request, 'my_orders.html', context)

@login_required
def account_settings(request):
    customer = request.user.customer_profile
    context = {
        'customer': customer
    }
    return render(request, 'account_settings.html', context)

@login_required
def update_profile(request):
    customer = request.user.customer_profile
    if request.method == 'POST':
        customer.customer_name = request.POST.get('full_name')
        customer.user.email = request.POST.get('email')
        customer.customer_phone_number = request.POST.get('phone_number')
        customer.customer_address = request.POST.get('address')
        customer.customer_state = request.POST.get('state')
        customer.customer_ic = request.POST.get('ic_no')
        # ... Validate and save the data ...
        customer.save()
        customer.user.save()
        messages.success(request, 'Your profile has been updated.')
        return redirect('account_settings')
    else:
        return render(request, 'edit_profile.html', {'customer': customer})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account_settings')  # Redirect to the account settings page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})




