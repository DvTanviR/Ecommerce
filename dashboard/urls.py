from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', staff_member_required(views.home), name='dashboard'),
    path('products/', staff_member_required(views.products), name='products'),
    path('product/add/', staff_member_required(views.add_product), name='add_product'),
    path('product/edit/<int:pk>/', staff_member_required(views.edit_product), name='edit_product'),
    path('product/delete/<int:pk>/', staff_member_required(views.delete_product), name='delete_product'),
    path('product/image/<int:pk>/delete/', staff_member_required(views.delete_product_image), name='delete_product_image'),
    path('orders/', staff_member_required(views.orders), name='orders'),
    path('order/<str:order_type>/<int:pk>/', staff_member_required(views.order_details), name='order_details'),
    path('order/delete/<int:pk>/', staff_member_required(views.delete_order), name='delete_order'),
    path('customers/', staff_member_required(views.customers), name='customers'),
    path('customer/<int:pk>/', staff_member_required(views.customer_details), name='customer_details'),
    path('customer/delete/<int:pk>/', staff_member_required(views.delete_customer), name='delete_customer'),
    path('categories/', staff_member_required(views.categories), name='categories'),
    path('category/add/', staff_member_required(views.add_category), name='add_category'),
    path('category/edit/<int:pk>/', staff_member_required(views.edit_category), name='edit_category'),
    path('category/delete/<int:pk>/', staff_member_required(views.delete_category), name='delete_category'),
    
    
    # Blog management URLs
    path('blogs/', staff_member_required(views.blogs), name='blogs'),
    path('blog/add/', staff_member_required(views.add_blog), name='add_blog'),
    path('blog/edit/<int:pk>/', staff_member_required(views.edit_blog), name='edit_blog'),
    path('blog/delete/<int:pk>/', staff_member_required(views.delete_blog), name='delete_blog'),
    path('blog/category/add/', staff_member_required(views.add_blog_category), name='add_blog_category'),
    path('blog/tag/add/', staff_member_required(views.add_blog_tag), name='add_blog_tag'),
    path('comments/', staff_member_required(views.comments), name='comments'),
    path('comment/approve/<int:pk>/', staff_member_required(views.approve_comment), name='approve_comment'),
    path('comment/delete/<int:pk>/', staff_member_required(views.delete_comment), name='delete_comment'),

    # Review management URLs
    path('reviews/', staff_member_required(views.reviews), name='dashboard_reviews'),
    path('review/approve/<int:pk>/', staff_member_required(views.approve_review), name='approve_review'),
    path('review/delete/<int:pk>/', staff_member_required(views.delete_review), name='delete_review'),
    path('review/<int:pk>/', staff_member_required(views.review_details), name='review_details'),

    # Template management URLs
    path('template/', staff_member_required(views.template_page), name='template'),

    # CoverSell CRUD
    path('template/cover/add/', staff_member_required(views.add_cover), name='add_cover'),
    path('template/cover/edit/<int:pk>/', staff_member_required(views.edit_cover), name='edit_cover'),
    path('template/cover/delete/<int:pk>/', staff_member_required(views.delete_cover), name='delete_cover'),

    # TrendCover edit only
    path('template/trend/edit/', staff_member_required(views.edit_trend_cover), name='edit_trend_cover'),

    # FlashDeal edit only
    path('template/flash/edit/', staff_member_required(views.edit_flash_deal), name='edit_flash_deal'),

    # FeaturedProduct edit only
    path('template/featured/edit/<int:pk>/', staff_member_required(views.edit_featured_product), name='edit_featured_product'),
]