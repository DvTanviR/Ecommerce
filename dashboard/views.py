from .forms import CoverSellForm, TrendCoverForm, FeaturedProductForm, FlashDealForm
from django.shortcuts import render, redirect, get_object_or_404
from main.models import *
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm, BlogForm
from django.utils.text import slugify
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.forms import modelformset_factory
from main.models import Product, ProductImage, Catagory as Category, CoverSell, TrendCover, FeaturedProduct, FlashDeal

# Create your views here.
@staff_member_required
def home(request):
    latest_orders = Order.objects.all().order_by('-date')[:5]
    latest_products = Product.objects.all().order_by('-pub_date')[:5]
    latest_customers = User.objects.all().order_by('-date_joined')[:5]
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = User.objects.count()
    total_revenue = sum(float(order.product.price) for order in Order.objects.all() if order.product is not None)
    context = {
        'page': 'home',
        'orders': latest_orders,
        'products': latest_products,
        'customers': latest_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_revenue': total_revenue
    }
    return render(request, 'dashboard/pages/home.html', context)

@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('products')

@staff_member_required
def products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(taitle__icontains=query)
    else:
        products = Product.objects.all()
    form = ProductForm()
    context = {
        'page': 'products',
        'products': products,
        'form': form
    }
    return render(request, 'dashboard/pages/products.html', context)

@staff_member_required
def orders(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    order_type = request.GET.get('type', 'all')
    
    # Get both regular orders and cart orders
    regular_orders = Order.objects.all().order_by('-date')
    cart_orders = CartOrder.objects.all().order_by('-date')  # Changed from order_date to date
    
    if query:
        regular_orders = regular_orders.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(product__taitle__icontains=query)
        )
        cart_orders = cart_orders.filter(
            Q(user__email__icontains=query) |
            Q(user__name__icontains=query)
        )
    
    if status:
        regular_orders = regular_orders.filter(status=status)
        cart_orders = cart_orders.filter(status=status)  # Changed from order_status to status
    
    # Filter by order type
    if order_type == 'regular':
        orders = regular_orders
    elif order_type == 'card':
        orders = cart_orders
    else:
        # Combine both types and add a type indicator
        orders = []
        for order in regular_orders:
            orders.append({'order': order, 'type': 'regular'})
        for order in cart_orders:
            orders.append({'order': order, 'type': 'card'})
        # Sort by date
        orders.sort(key=lambda x: x['order'].date, reverse=True)
    
    context = {
        'orders': orders,
        'page': 'orders',
        'order_type': order_type,
        'current_status': status,
    }
    return render(request, 'dashboard/pages/orders.html', context)

@staff_member_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('orders')

@staff_member_required
def order_details(request, order_type, pk):
    if order_type == 'regular':
        order = get_object_or_404(Order, pk=pk)
        status_choices = Order._meta.get_field('status').choices
        template = 'dashboard/pages/order_details.html'
    else:
        order = get_object_or_404(CartOrder, pk=pk)
        status_choices = CartOrder._meta.get_field('status').choices  # Changed from order_status to status
        template = 'dashboard/pages/card_order_details.html'
    
    if request.method == 'POST':
        if order_type == 'regular':
            order.status = request.POST.get('status')
        else:
            order.status = request.POST.get('status')  # Changed from order_status to status
        order.save()
        messages.success(request, 'Order status updated successfully!')
        return redirect('orders')
        
    context = {
        'order': order,
        'status_choices': status_choices,
        'order_type': order_type,
    }
    return render(request, template, context)

@staff_member_required
def customers(request):
    query = request.GET.get('q')
    if query:
        customers = User.objects.filter(
            Q(email__icontains=query) |
            Q(name__icontains=query)
        )
    else:
        customers = User.objects.all()
    context = {
        'customers': customers,
        'page': 'customers'
    }
    return render(request, 'dashboard/pages/customers.html', context)

@staff_member_required
def delete_customer(request, pk):
    customer = get_object_or_404(User, pk=pk)
    customer.delete()
    return redirect('customers')

@staff_member_required
def customer_details(request, pk):
    customer = get_object_or_404(User, pk=pk)
    return render(request, 'dashboard/pages/customer_details.html', {'customer': customer})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                
                # Handle description and info from Quill editor
                product.dicription = request.POST.get('dicription')
                product.info = request.POST.get('info')
                product.save()
                
                # Handle multiple images
                images = request.FILES.getlist('images')
                for i, image in enumerate(images[:5]):  # Limit to 5 images
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_main=i == 0  # First image is the main image
                    )
                
                messages.success(request, 'Product added successfully!')
                return redirect('products')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            messages.error(request, f'Error saving product: {str(e)}')
    return redirect('products')

@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                # Handle description and info from Quill editor or POST
                product.dicription = request.POST.get('dicription', product.dicription)
                product.info = request.POST.get('info', product.info)
                product.save()

                # Handle new images (add up to 5 total)
                images = request.FILES.getlist('images')
                current_images = product.productimage_set.count()
                for i, image in enumerate(images[:max(0, 5-current_images)]):
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_main=(current_images == 0 and i == 0)
                    )

                messages.success(request, 'Product updated successfully!')
                return redirect('products')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/pages/edit_product.html', {
        'form': form,
        'product': product,
        'product_images': product.productimage_set.all()
    })

@staff_member_required
def delete_product_image(request, pk):
    if request.method == 'POST':
        image = get_object_or_404(ProductImage, pk=pk)
        product = image.product
        was_main = image.is_main
        image.delete()
        
        # If we deleted the main image, make the first remaining image the main one
        if was_main and product.productimage_set.exists():
            new_main = product.productimage_set.first()
            new_main.is_main = True
            new_main.save()
            
        messages.success(request, 'Image deleted successfully!')
        return redirect('edit_product', pk=product.pk)
    return redirect('dashboard')

@staff_member_required
def blogs(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__name__icontains=query)
        )
    else:
        blogs = Blog.objects.all().order_by('-created_date')
    form = BlogForm()
    context = {
        'page': 'blogs',
        'blogs': blogs,
        'form': form
    }
    return render(request, 'dashboard/pages/blogs.html', context)

@staff_member_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.slug = slugify(blog.title)
            blog.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Blog post created successfully!')
            return redirect('blogs')
        else:
            # Add form error messages for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = BlogForm()
    return render(request, 'dashboard/pages/add_blog.html', {'form': form, 'page': 'blogs'})

@staff_member_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(blog.title)
            # Ensure the content is properly saved
            if 'content' in request.POST:
                blog.content = request.POST['content']
            blog.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blogs')
        else:
            # Add form error messages for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
                    print(f'Form error in {field}: {error}')  # Debug print
            print(f'POST data: {request.POST}')  # Debug print
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'dashboard/pages/edit_blog.html', {'form': form, 'blog': blog})

@staff_member_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect('blogs')

@staff_member_required
def comments(request):
    query = request.GET.get('q')
    if query:
        comments = BlogComment.objects.filter(
            Q(content__icontains=query) |
            Q(user__name__icontains=query) |
            Q(blog__title__icontains=query)
        )
    else:
        comments = BlogComment.objects.all().order_by('-created_date')
    context = {
        'page': 'comments',
        'comments': comments,
    }
    return render(request, 'dashboard/pages/comments.html', context)

@staff_member_required
def approve_comment(request, pk):
    comment = get_object_or_404(BlogComment, pk=pk)
    comment.is_approved = not comment.is_approved
    comment.save()
    messages.success(request, f'Comment {"approved" if comment.is_approved else "unapproved"} successfully!')
    return redirect('comments')

@staff_member_required
def delete_comment(request, pk):
    comment = get_object_or_404(BlogComment, pk=pk)
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('comments')

@staff_member_required
def add_blog_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            try:
                # Check if category already exists
                if BlogCategory.objects.filter(name=name).exists():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'A category with this name already exists.'
                    })
                
                category = BlogCategory.objects.create(
                    name=name,
                    description=description,
                    slug=slugify(name)
                )
                return JsonResponse({
                    'status': 'success',
                    'id': category.id,
                    'name': category.name
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or missing data'
    })

@staff_member_required
def add_blog_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                # Check if tag already exists
                if Tag.objects.filter(name=name).exists():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'A tag with this name already exists.'
                    })
                    
                tag = Tag.objects.create(
                    name=name,
                    slug=slugify(name)
                )
                return JsonResponse({
                    'status': 'success',
                    'id': tag.id,
                    'name': tag.name
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or missing data'
    })

@staff_member_required
def reviews(request):
    query = request.GET.get('q')
    verified = request.GET.get('verified')
    
    reviews = ProductReview.objects.all()
    
    if query:
        reviews = reviews.filter(
            Q(customer_name__icontains=query) |
            Q(review__icontains=query) |
            Q(product__taitle__icontains=query)
        )
    
    if verified is not None:
        is_verified = verified.lower() == 'true'
        reviews = reviews.filter(is_verified=is_verified)
        
    reviews = reviews.order_by('-created_at')
    
    context = {
        'page': 'reviews',
        'reviews': reviews,
    }
    return render(request, 'dashboard/pages/reviews.html', context)

@staff_member_required
def review_details(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)
    return render(request, 'dashboard/pages/review_details.html', {'review': review})

@staff_member_required
def approve_review(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)
    review.is_verified = not review.is_verified
    review.save()
    messages.success(request, f'Review {"approved" if review.is_verified else "unapproved"} successfully!')
    return redirect('dashboard_reviews')

@staff_member_required
def delete_review(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('dashboard_reviews')

@staff_member_required
def categories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            if Category.objects.filter(name=name).exists():
                messages.error(request, 'Category with this name already exists.')
            else:
                Category.objects.create(
                    name=name,
                    description=description,
                    slug=slugify(name)
                )
                messages.success(request, 'Category added successfully!')
        else:
            messages.error(request, 'Name is required to add a category.')
        return redirect('categories')

    query = request.GET.get('q')
    if query:
        categories = Category.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all().order_by('-id')
    context = {
        'page': 'categories',
        'categories': categories
    }
    return render(request, 'dashboard/pages/categories.html', context)

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories')

@staff_member_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            if Category.objects.filter(name=name).exclude(pk=pk).exists():
                messages.error(request, 'Another category with this name already exists.')
            else:
                category.name = name
                category.description = description
                category.slug = slugify(name)
                category.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('categories')
        else:
            messages.error(request, 'Name is required to update the category.')
    
    return render(request, 'dashboard/pages/edit_category.html', {'category': category,  'page': 'categories',})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories')

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            if Category.objects.filter(name=name).exists():
                messages.error(request, 'Category with this name already exists.')
            else:
                Category.objects.create(
                    name=name,
                    image= request.FILES.get('image'),
                )
                messages.success(request, 'Category added successfully!')
        else:
            messages.error(request, 'Name is required to add a category.')
        return redirect('categories')
    return render(request, 'dashboard/pages/add_category.html', { 'page': 'categories'})


# Template Page Views
@staff_member_required
def template_page(request):
    covers = CoverSell.objects.all().order_by('-id')
    try:
        trend_cover = TrendCover.objects.first()
    except TrendCover.DoesNotExist:
        trend_cover = None
    flash_deal = FlashDeal.objects.first()
    featured_products = FeaturedProduct.objects.all()
    context = {
        'covers': covers,
        'trend_cover': trend_cover,
        'flash_deal': flash_deal,
        'featured_products': featured_products,
        'page': 'template',
    }
    return render(request, 'dashboard/pages/template.html', context)

# CoverSell CRUD
@staff_member_required
def add_cover(request):
    if request.method == 'POST':
        form = CoverSellForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cover added successfully!')
            return redirect('template_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CoverSellForm()
    return render(request, 'dashboard/pages/add_cover.html', {'form': form, 'page': 'template'})

@staff_member_required
def edit_cover(request, pk):
    cover = get_object_or_404(CoverSell, pk=pk)
    if request.method == 'POST':
        form = CoverSellForm(request.POST, request.FILES, instance=cover)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cover updated successfully!')
            return redirect('template_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CoverSellForm(instance=cover)
    return render(request, 'dashboard/pages/edit_cover.html', {'form': form, 'cover': cover, 'page': 'template'})

@staff_member_required
def delete_cover(request, pk):
    cover = get_object_or_404(CoverSell, pk=pk)
    cover.delete()
    messages.success(request, 'Cover deleted successfully!')
    return redirect('template_page')

# TrendCover Edit Only
@staff_member_required
def edit_trend_cover(request):
    trend_cover = TrendCover.objects.first()
    if not trend_cover:
        messages.error(request, 'No TrendCover found.')
        return redirect('template_page')
    if request.method == 'POST':
        form = TrendCoverForm(request.POST, request.FILES, instance=trend_cover)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trend cover updated successfully!')
            return redirect('template_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TrendCoverForm(instance=trend_cover)
    return render(request, 'dashboard/pages/edit_trend_cover.html', {'form': form, 'trend_cover': trend_cover, 'page': 'template'})

# FeaturedProduct Edit Only
@staff_member_required
def edit_featured_product(request, pk):
    featured_product = get_object_or_404(FeaturedProduct, pk=pk)
    if request.method == 'POST':
        form = FeaturedProductForm(request.POST, request.FILES, instance=featured_product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Featured product updated successfully!')
            return redirect('template_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = FeaturedProductForm(instance=featured_product)
    return render(request, 'dashboard/pages/edit_featured_product.html', {'form': form, 'featured_product': featured_product, 'page': 'template'})

# FlashDeal Management
@staff_member_required
def edit_flash_deal(request):
    """Edit the existing FlashDeal or create one if it doesn't exist"""
    flash_deal = FlashDeal.objects.first()
    is_new = not flash_deal
    
    if request.method == 'POST':
        form = FlashDealForm(request.POST, request.FILES, instance=flash_deal)
        if form.is_valid():
            form.save()
            if is_new:
                messages.success(request, 'Flash deal created successfully!')
            else:
                messages.success(request, 'Flash deal updated successfully!')
            return redirect('template_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = FlashDealForm(instance=flash_deal)
    
    return render(request, 'dashboard/pages/edit_flash_deal.html', {
        'form': form,
        'flash_deal': flash_deal,
        'is_new': is_new,
        'page': 'template'
    })