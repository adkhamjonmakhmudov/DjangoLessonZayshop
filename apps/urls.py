from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import HomePageTemplateView, AboutPageTemplateView, ShopTemplateView, ContactPageTemplateView, \
    ProductDetailView, UserProductCreateView, CustomLoginView, RegisterView, CategoryProductsView

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='index'),
    path('about/', AboutPageTemplateView.as_view(), name='about'),
    path('shop/', ShopTemplateView.as_view(), name='shop'),
    path('contact/', ContactPageTemplateView.as_view(), name='contact'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='shop_detail'),
    path('create/', UserProductCreateView.as_view(), name='create'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('category/<slug:slug>/', CategoryProductsView.as_view(), name='category_products'),

]
