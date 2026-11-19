from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
)

urlpatterns = [
    path('', CartView.as_view(), name='view-cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('update/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart'),
    path('remove/<int:pk>/', RemoveCartItemView.as_view(), name='remove-cart'),
]