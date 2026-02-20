from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['taitle', 'catagory', 'price']
    prepopulated_fields = {'slug': ('taitle',)}
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Catagory)
admin.site.register(CoverSell)
admin.site.register(Order)
#admin.site.register(Cart)
#admin.site.register(Wishlist)
#admin.site.register(FavouriteCatagory)
#admin.site.register(Subscriber)
admin.site.register(Reveaws)
admin.site.register(FlashDeal)
admin.site.register(TrendCover)
#admin.site.register(Contact)
admin.site.register(FeaturedProduct)
admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(ProductReview)
admin.site.register(CartOrder)
@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created_date', 'is_approved')
    list_filter = ('is_approved', 'created_date')
    search_fields = ('user__name', 'blog__title', 'content')
    actions = ['approve_comments', 'unapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_comments.short_description = "Unapprove selected comments"