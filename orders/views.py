from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem
from .forms import CheckoutForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'orders/menu.html', {'items': items})




@login_required
@require_POST
def ajax_add_to_cart(request):
    menu_item_id = request.POST.get('menu_item_id')
    if not menu_item_id:
        return JsonResponse({'error': 'Missing menu_item_id'}, status=400)

    item = get_object_or_404(MenuItem, id=menu_item_id)

    order, created = Order.objects.get_or_create(user=request.user, status='Pending')

    order_item, created = OrderItem.objects.get_or_create(order=order, menu_item=item)
    if not created:
        order_item.quantity += 1
        order_item.save()

    return JsonResponse({'message': f'Added {item.name} to cart!'})



@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, status='Pending').first()
    cart_items = []
    cart_total = 0

    if order:
        cart_items = OrderItem.objects.filter(order=order)
        for item in cart_items:
            item.subtotal = item.menu_item.price * item.quantity
        cart_total = sum(item.subtotal for item in cart_items)

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, status='Pending').first()
    if not order:
        return redirect('menu')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order.customer_email = form.cleaned_data['customer_email']
            order.delivery_address = form.cleaned_data['delivery_address']
            order.delivery_lat = form.cleaned_data['delivery_lat']
            order.delivery_lng = form.cleaned_data['delivery_lng']
            order.status = 'Submitted'
            order.save()
            return redirect('order_confirmation')
    else:
        initial_data = {
            'customer_email': request.user.email if request.user.is_authenticated else '',
            'delivery_address': order.delivery_address or '',
            'delivery_lat': order.delivery_lat or None,
            'delivery_lng': order.delivery_lng or None,
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {'form': form})



@login_required
def order_confirmation(request):
    return render(request, 'orders/order_confirmation.html')


@login_required
@require_POST
def update_cart(request, menu_item_id):
    action = request.POST.get('action')
    item = get_object_or_404(MenuItem, id=menu_item_id)
    order = Order.objects.get(user=request.user, status='Pending')

    try:
        order_item = OrderItem.objects.get(order=order, menu_item=item)
    except OrderItem.DoesNotExist:
        return redirect('view_cart')

    if action == "increase":
        order_item.quantity += 1
    elif action == "decrease":
        if order_item.quantity > 1:
            order_item.quantity -= 1
    order_item.save()

    return redirect('view_cart')


@login_required
@require_POST
def ajax_remove_from_cart(request):
    menu_item_id = request.POST.get('menu_item_id')
    if not menu_item_id:
        return JsonResponse({'error': 'No menu item ID provided'}, status=400)

    item = get_object_or_404(MenuItem, id=menu_item_id)
    order = Order.objects.filter(user=request.user, status='Pending').first()
    if not order:
        return JsonResponse({'error': 'No active order'}, status=400)

    try:
        order_item = OrderItem.objects.get(order=order, menu_item=item)
        order_item.delete()
    except OrderItem.DoesNotExist:
        return JsonResponse({'error': 'Item not in cart'}, status=404)

    return JsonResponse({
        'message': 'Item removed from cart',
        'total': float(order.total_price()),
    })



@login_required
@require_POST
def ajax_update_cart(request):
    menu_item_id = request.POST.get('menu_item_id')
    action = request.POST.get('action')

    if not menu_item_id or not action:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    item = get_object_or_404(MenuItem, id=menu_item_id)
    order = Order.objects.filter(user=request.user, status='Pending').first()
    if not order:
        return JsonResponse({'error': 'No active order'}, status=400)

    try:
        order_item = OrderItem.objects.get(order=order, menu_item=item)
    except OrderItem.DoesNotExist:
        return JsonResponse({'error': 'Item not in cart'}, status=404)

    if action == "increase":
        order_item.quantity += 1
        order_item.save()
    elif action == "decrease":
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
    elif action == "remove":
        order_item.delete()
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

    return JsonResponse({
        'quantity': order_item.quantity if action != "remove" else 0,
        'subtotal': float(order_item.menu_item.price * order_item.quantity) if action != "remove" else 0,
        'total': float(order.total_price()),
        'item_name': order_item.menu_item.name,
    })



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')
    else:
        form = UserCreationForm()
    return render(request, 'orders/signup.html', {'form': form})
