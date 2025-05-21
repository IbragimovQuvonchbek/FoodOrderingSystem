from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem
from .forms import CheckoutForm
from django.views.decorators.http import require_POST



def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'orders/menu.html', {'items': items})


def add_to_cart(request, menu_item_id):
    item = get_object_or_404(MenuItem, id=menu_item_id)
    cart = request.session.get('cart', {})
    cart[str(menu_item_id)] = cart.get(str(menu_item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')  # now goes directly to cart page


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, quantity in cart.items():
        menu_item = get_object_or_404(MenuItem, id=item_id)
        subtotal = menu_item.price * quantity
        cart_items.append({
            'menu_item': menu_item,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    context = {
        'cart_items': cart_items,
        'cart_total': total,
    }
    return render(request, 'orders/cart.html', context)


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_email=form.cleaned_data['customer_email'],
                user=request.user if request.user.is_authenticated else None
            )
            for item_id, quantity in cart.items():
                menu_item = get_object_or_404(MenuItem, id=item_id)
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)

            request.session['cart'] = {}  # clear cart
            return redirect('order_confirmation')
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})


def order_confirmation(request):
    return render(request, 'orders/order_confirmation.html')


@require_POST
def update_cart(request, menu_item_id):
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    item_id_str = str(menu_item_id)

    if item_id_str in cart:
        if action == "increase":
            cart[item_id_str] += 1
        elif action == "decrease":
            cart[item_id_str] = max(1, cart[item_id_str] - 1)
    request.session['cart'] = cart
    return redirect('view_cart')

@require_POST
def remove_from_cart(request, menu_item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(menu_item_id)
    if item_id_str in cart:
        del cart[item_id_str]
    request.session['cart'] = cart
    return redirect('view_cart')
