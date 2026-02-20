from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutpage, name='logout'),

    path('my-account-dashboard/', views.accountDashbord, name='account'),

    path('product/<slug:slug>/', views.product, name='product'),

    path('product/<slug:slug>/place-order/', views.OrderPage, name='order'),
    path('order-cancle/<int:pk>/', views.cancleOrder, name='cancle_order'),
    path('product/<slug:slug>/review/', views.reveawPage, name='product_review'),

    path('shop/', views.shopPage, name='shop'),
    path('top-prducts/', views.topPage, name='top'),
    path('sell/', views.sellPage, name='sell'),

    path('cart/', views.cartPage, name="cart"),
    path('product/add-cart/<slug:slug>/', views.addCart, name='add_cart'),
    path('delete-cart/<int:pk>/',views.deleteCart, name="delete_cart"),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),

    path('wishlist/', views.wishlistPage, name='wishlist'),
    path('product/add-wishlist/<slug:slug>/', views.addWishlist, name='add_wishlist'),
    path('delete-wishlist/<int:pk>/', views.deleteWishlist, name="delete_wishlist"),

    path('contact/', views.contactPage, name="contact"),
    path('about/', views.aboutPage, name="about"),
    path('blog/', views.blogPage, name="blog"),
    path('blog/<slug:slug>/', views.blogDetailPage, name="blog_detail"),

    path('privacy-policy/', views.privecyPage, name="privecy"),
    path('terms-and-conditions/', views.termsPage, name="terms"),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='password/check_email.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/reset.html'), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/done.html'), name="password_reset_complete"),

    path('maillatter/', views.mailLatter, name="mailsender"),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
   
    path('reviews/', views.create_review_link, name='create_review_link'),
]