from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from .forms import ContactForm
from myapp.models import CustomUser
from django.contrib import messages
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem
from django.contrib import messages
from django.shortcuts import render
from .models import Order
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import OrderItem

from django.shortcuts import render
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Order


def home(request):
    """Render the homepage with product details."""
    products = Product.objects.all()  # Fetch all products
    return render(request, 'home.html', {'products': products})



def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        password = request.POST['password']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_user')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_user')

        # Create a new user with default user_type as 'user'
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            user_type='user'
        )
        user.save()
        messages.success(request, "User registration successful. Please log in.")
        return redirect('login')
    
    return render(request, 'reg.html')


def register_seller(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        password = request.POST['password']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('sellerregister')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('sellerregister')

        # Create a new seller with user_type as 'seller'
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            user_type='seller'
        )
        user.save()
        messages.success(request, "Seller registration successful. Please log in.")
        return redirect('login')
    
    return render(request, 'sellerregister.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.is_superuser == 1:
              
                return redirect('admin_dashboard')
            elif user.user_type == 'seller':
                # return HttpResponse('seller')
                return redirect('dashboard')
            elif user.user_type == 'user':
                # return HttpResponse('user')
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def about(request):
    return render(request, 'aboutpage.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email
            send_mail(
                subject,
                message,
                email,
                ['amiljithjs@gmail.com'],  # Replace with your email or list of recipient emails
            )
            
            return HttpResponse('Thank you for your message.')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the home page after logout


@login_required
def profile_view(request):
    User = get_user_model()
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        user = None
    return render(request, 'profile.html', {'user': user})


@login_required
def dashboard(request):
    """Render the seller dashboard."""
    user = request.user
  
    # Total products added by the seller
    total_products = Product.objects.filter(seller=user).count()
    print(f"Total Products: {total_products}")

    # Total orders for the seller's products
    total_orders = OrderItem.objects.filter(product__seller=user).count()
    print(f"Total Orders: {total_orders}")

    # Total sales for the seller's products
    order_items = OrderItem.objects.filter(product__seller=user)
    print(f"Order Items: {order_items}")



    total_sales = sum(item.total_price for item in order_items)
    print(f"Total Sales: {total_sales}")

    # total_sales = OrderItem.objects.filter(product__seller=user).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
    }
    return render(request, 'sellerdash.html', context)


@login_required
def add_product(request):
    """Handle adding a new product."""
    if request.method == 'POST':
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        price = request.POST.get('product_price')
        image = request.FILES.get('product_image')

        # Validation: Ensure all required fields are provided
        if not (name and description and price and image):
            messages.error(request, 'All fields are required.')
            return redirect('add_product')

        # Create and save product instance
        product = Product(
            seller=request.user,
            name=name,
            description=description,
            price=price,
            image=image
        )
        product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('dashboard')

    return render(request, 'selleraddproduct.html')






@login_required
def manage_products(request):
    """List all products for the logged-in seller."""
    products = Product.objects.filter(seller=request.user)
    context = {'products': products}
    return render(request, 'manage_products.html', context)

@login_required
def edit_product(request, product_id):
    """Edit an existing product."""
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        product.name = request.POST.get('product_name')
        product.description = request.POST.get('product_description')
        product.price = request.POST.get('product_price')

        if 'product_image' in request.FILES:
            product.image = request.FILES['product_image']

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('manage_products')

    context = {'product': product}
    return render(request, 'edit_product.html', context)

@login_required
def delete_product(request, product_id):
    """Delete an existing product."""
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('manage_products')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} added to cart successfully!")
    return redirect(request.META.get("HTTP_REFERER", "home"))
    # return redirect('home')
    # return HttpResponse("<script>alert('Added to cart successfully!');window.location.href=document.referrer;</script>")

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def add_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def subtract_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')



@login_required
def order_form(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Add products before placing an order.")
        return redirect('cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        total_price = sum(item.get_total_price() for item in cart_items)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            total_price=total_price
        )

        # Add items to the order
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        # Clear the cart
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_confirmation')

    return render(request, 'order_form.html', {'cart_items': cart_items})


@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')



def view_orders(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)
    
    # If you want to pass the related order items as well
    order_details = []
    for order in orders:
        order_details.append({
            'order': order,
            'orderitems': order.orderitem_set.all()  # Adjust if you're using related_name
        })
    
    return render(request, 'orders.html', {'order_details': order_details})

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('view_orders')  # Redirect to the orders page


from django.shortcuts import render
from .models import Product

def search_products(request):
    query = request.GET.get('query', '')  # Get the search term from the query string
    products = Product.objects.all()

    if query:
        # Filter products based on the name or description containing the search term (case insensitive)
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'search_results.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import OrderItem

@login_required
def view_orders_for_seller(request):
    """View all orders for the products sold by the logged-in seller."""
    seller = request.user

    # Fetch all OrderItems where the product is sold by the current seller
    order_items = OrderItem.objects.filter(product__seller=seller)

    # Group the order items by their respective orders
    orders = {}
    for item in order_items:
        if item.order.id not in orders:
            orders[item.order.id] = {
                'order': item.order,
                'items': [],
                'customer': {
                    'username': item.order.user.username,
                    'email': item.order.user.email,
                    'full_name': item.order.full_name,
                },
                'address': {
                    'address': item.order.address,
                    'city': item.order.city,
                    'state': item.order.state,
                    'postal_code': item.order.postal_code,
                }
            }
        orders[item.order.id]['items'].append(item)

    # Pass the grouped orders to the template
    context = {'orders': orders.values()}
    return render(request, 'sellerorders.html', context)

 


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserProfileForm  # You need to create a form for profile editing.

# View to display the user profile
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# View to handle editing of the user profile
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  # Redirect back to the profile view
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'edit_profile.html', {'form': form})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, Order, CustomUser, OrderItem

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, Order, CustomUser

def adminbase(request):
    return render(request, 'adminbase.html')

@login_required
def admin_dashboard(request):
    """Render a custom admin dashboard with seller details."""
    # Summary Data
    total_users = CustomUser.objects.count()
    total_sellers = CustomUser.objects.filter(user_type='seller').count()
    total_orders = Order.objects.count()
    total_revenue = sum(order.total_price for order in Order.objects.all())
    total_products = Product.objects.count()

    # Recent Orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    # Seller Details
    sellers = CustomUser.objects.filter(user_type='seller').order_by('-date_joined')

    context = {
        'total_users': total_users,
        'total_sellers': total_sellers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'sellers': sellers,
    }
    return render(request, 'admin_dashboard.html', context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def seller_list(request):
    sellers = CustomUser.objects.filter(user_type='seller').order_by('-date_joined')
    return render(request, 'seller_list.html', {'sellers': sellers})


@login_required
def user_list(request):
    users = CustomUser.objects.filter(user_type='user').order_by('-date_joined')
    return render(request, 'user_list.html', {'users': users})









from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def user_list(request):
    """Render a page showing all users."""
    users = CustomUser.objects.filter(user_type='user').order_by('-date_joined')
    context = {
        'users': users,
        'title': 'User List',
    }
    return render(request, 'user_list.html', context)

@login_required
def seller_list(request):
    """Render a page showing all sellers."""
    sellers = CustomUser.objects.filter(user_type='seller').order_by('-date_joined')
    context = {
        'sellers': sellers,
        'title': 'Seller List',
    }
    return render(request, 'seller_list.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def admin_order_detail(request, order_id):
    """View to display the details of a specific order for the admin."""
    # Fetch the order with the given ID or return a 404 if it doesn't exist
    order = get_object_or_404(Order, id=order_id)

    # Fetch all items related to the order
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'admin_order_list.html', context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def block_seller(request, seller_id):
    """Block a seller by setting is_active to False."""
    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller')
    if seller.is_active:
        seller.is_active = False
        seller.save()
        messages.success(request, f'Seller {seller.username} has been blocked.')
    else:
        messages.warning(request, f'Seller {seller.username} is already blocked.')
    return redirect('seller_list')  # Redirect back to seller list

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def unblock_seller(request, seller_id):
    """Unblock a seller by setting is_active to True."""
    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller')

    # Debugging: Print current status
    print(f"Unblocking Seller: {seller.username}, Current Status: {seller.is_active}")

    if not seller.is_active:
        seller.is_active = True
        seller.save()

        # Debugging: Check if change was saved
        updated_seller = CustomUser.objects.get(id=seller_id)
        print(f"New Status: {updated_seller.is_active}")

        messages.success(request, f'Seller {seller.username} has been unblocked.')
    else:
        messages.warning(request, f'Seller {seller.username} is already active.')

    return redirect('seller_list')  # Ensure 'seller_list' is a valid URL name

















