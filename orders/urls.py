from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('ajax/add-to-cart/', views.ajax_add_to_cart, name='ajax_add_to_cart'),  # You can keep this for initial add, or convert this to AJAX as well
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),

    # Removed traditional update/remove cart URLs:
    # path('update-cart/<int:menu_item_id>/', views.update_cart, name='update_cart'),
    # path('remove-from-cart/<int:menu_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Keep AJAX endpoint for cart updates (increase, decrease, remove can be handled via POST data 'action'):
    path('ajax/update-cart/', views.ajax_update_cart, name='ajax_update_cart'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='menu'), name='logout'),
]
