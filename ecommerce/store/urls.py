from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('updateItem/', views.updateItem,name='updateItem'),
    path('processOrder/', views.processOrder,name='processOrder'),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)