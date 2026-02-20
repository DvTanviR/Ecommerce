from django.shortcuts import redirect, render
from .models import *
from django.db.models import Q, Sum, Avg, Count
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .forms import MyUserCreationForm, UserEditForm, FavouriteForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Max
from django.http import JsonResponse

#if super user function
# @user_passes_test(lambda u: u.is_superuser)
# def my_view(request):


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = MyUserCreationForm()

    if request.method=='POST':
        if request.POST.get("form_type") == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)    
            except:
                messages.error(request, "User does not exist!")
                return render(request, 'home/login.html', {'form': form})

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Merge cart items from session to user's cart
                session_cart = request.session.get('cart', {})
                for item_id, item_data in session_cart.items():
                    product = Product.objects.get(id=int(item_id))
                    # Check if product already in user's cart
                    if not Cart.objects.filter(host=user, product=product).exists():
                        Cart.objects.create(
                            product=product,
                            host=user
                        )
                
                # Clear session cart after merging
                if 'cart' in request.session:
                    del request.session['cart']
                    request.session.modified = True
                
                return redirect('home')
            else:
                messages.error(request, "Username or password does not exist")

        if request.POST.get("form_type") == 'register':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                Subscriber.objects.create(email=user.email)
                user.save()
                login(request, user)
                return redirect('home')
            else:
                for field in form:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")

    context = {'form': form}
    return render(request, 'home/login.html', context)

@login_required(login_url='login')
def logoutpage(request):
    logout(request)
    return redirect('home')



@login_required(login_url='login')
def accountDashbord(request):
    page= "dashboard"
    user= request.user
    #favouritecatagory= FavouriteCatagory.objects.get(pk=user.pk)
    form1= FavouriteForm(instance=user)
    user_id= request.user.pk
    user1= User.objects.get(pk=user_id)
    orders= user1.order_set.all()

    if request.method=="POST":
        if request.POST.get("form_type") == 'accountdetails':
            form= UserEditForm(request.POST, request.FILES ,instance=user)
            form1= FavouriteForm( request.POST, request.FILES,instance=user)
            try:
                if form1.is_valid:
                    user= form1.save(commit=False)
                    user.user= user
                    user.save()
                if form.is_valid:
                    form.save()
                    return redirect('account')
            except:
                messages.error(request, "Unvalid email or other data!")
            user1.name = request.POST.get('name')
            return redirect('account')


    context={
        'user':user,
        'fromus':form1,
        'orders': orders,
        'page':page,
    }
    return render(request, 'home/dashboard.html', context)




def product(request, slug):
    page = "shop"
    product = Product.objects.get(slug=slug)
    products = Product.objects.filter(
        Q(taitle__icontains=product.taitle) |
        Q(catagory__name__icontains=product.catagory) |
        Q(dicription__icontains=product.taitle)
    )[0:15]

    # Calculate ratings for the main product
    reveaw = product.reveaws_set.all()
    total_reviews = reveaw.count()
    average_rating = reveaw.aggregate(average_rating=Avg('rating'))['average_rating'] or 0

    # Add ratings for recommended products
    recommended_products = []
    for recommended_product in products:
        reviews = recommended_product.reveaws_set.all()
        recommended_total_reviews = reviews.count()
        recommended_average_rating = reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
        recommended_products.append({
            'product': recommended_product,
            'average_rating': recommended_average_rating,
            'total_reviews': recommended_total_reviews
        })

    context = {
        'product': product,
        'products': recommended_products,
        'reveaw': reveaw,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'page': page,
    }
    return render(request, 'home/product.html', context)




def home(request):
    page = "home"
    coversell = CoverSell.objects.all()  # Ensure this query returns data
    user = request.user
    sell = Product.objects.all()[0:20]
    bestselling = Product.objects.annotate(
        last_review=Max('order')
    ).order_by('-last_review')[0:20]
    fashdeal = FlashDeal.objects.first()  # Use first() instead of get() to avoid DoesNotExist error
    trendcatagory = Catagory.objects.all().order_by('-product')[0:1]
    toptrend = Product.objects.annotate(
        last_review=Max('reveaws__total'),
        average_rating=Avg('reveaws__rating'),
        total_reviews=Count('reveaws')
    ).order_by('-last_review')[0:20]

    # catagory content start
    catagory = Catagory.objects.annotate(
        last_review=Max('product')
    ).order_by('-last_review')[0:6]

    recomdation = Product.objects.filter(id__isnull=False).order_by('?')  # Ensure valid products
    recomdation_with_ratings = []
    for product in recomdation:
        reviews = product.reveaws_set.all()
        total_reviews = reviews.count()
        if total_reviews > 0:
            average_rating = reviews.aggregate(average_rating=Sum('rating') / total_reviews)['average_rating']
        else:
            average_rating = 0
        recomdation_with_ratings.append({
            'product': product,  # Ensure the product object is included
            'average_rating': average_rating,
            'total_reviews': total_reviews
        })

    # new arrival section
    newarivals = Product.objects.annotate(
        average_rating=Avg('reveaws__rating'),
        total_reviews=Count('reveaws')
    ).order_by('pub_date')
    trendcover = TrendCover.objects.first()  # Use first() instead of get() to avoid DoesNotExist error

    featuredproduct = FeaturedProduct.objects.all()[0:3]
    context = {
        'coversell': coversell,
        'catagory': catagory,
        'newarivals': newarivals,
        'user': user,
        'toptrend': toptrend,
        'sells': sell,
        'bestsell': bestselling,
        'recomdation': recomdation_with_ratings,
        'fashdeal': fashdeal,
        'trendcatagory': trendcatagory,
        'page': page,
        'trendcover': trendcover,
        'featuredproduct': featuredproduct,
    }
    return render(request, 'home/index.html', context)


def shopPage(request):
    pagE = "shop"
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    products = Product.objects.filter(
        Q(taitle__icontains=q) |
        Q(catagory__name__icontains=q) |
        Q(dicription__icontains=q)
    ).annotate(
        last_review=Max('reveaws__total'),
        average_rating=Avg('reveaws__rating'),
        total_reviews=Count('reveaws')
    ).order_by('-last_review')

    if request.method == 'POST':
        if request.POST.get('sortby') == "date":
            products = Product.objects.filter(
                Q(taitle__icontains=q) |
                Q(catagory__name__icontains=q) |
                Q(dicription__icontains=q)
            ).order_by('-pub_date')

        if request.POST.get('sortby') == "popularity":
            products = Product.objects.filter(
                Q(taitle__icontains=q) |
                Q(catagory__name__icontains=q) |
                Q(dicription__icontains=q)
            ).annotate(
                last_review=Max('reveaws__total'),
                average_rating=Avg('reveaws__rating'),
                total_reviews=Count('reveaws')
            ).order_by('-last_review')

    p = Paginator(products, 24)
    page = request.GET.get('page')
    productss = p.get_page(page)

    context = {
        'mainproduct': products,
        'products': productss,
        'page': pagE,
    }
    return render(request, 'home/shop.html', context)



def addCart(request, slug):
    if not request.POST.get('size') and not request.POST.get('quantity'):
        return redirect(request.META.get('HTTP_REFERER'))
        
    product = Product.objects.get(slug=slug)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        Cart.objects.create(
            product=product,
            host=request.user,
            size=size,
            quantity=quantity
        )
    else:
        cart = request.session.get('cart', {})
        product_id = str(product.id)
        
        if product_id not in cart:
            image_url = ''
            if product.productimage_set.exists():
                image_url = product.productimage_set.first().image.url
                
            cart[product_id] = {
                'id': product.id,
                'title': product.taitle,
                'price': product.price,
                'image': image_url,
                'slug': product.slug,
                'size': size,
                'quantity': quantity
            }
            request.session['cart'] = cart
            request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER'))


def cartPage(request):
    cart_items = []
    cart_total = 0

    if request.user.is_authenticated:
        # Existing logic for logged in users
        user = User.objects.get(pk=request.user.pk)
        cart_items = user.cart_set.all()
        cart_total = sum(float(item.product.price.replace('৳', '').replace('Tk', '').strip()) for item in cart_items)
    else:
        # Handle anonymous users with session
        cart = request.session.get('cart', {})
        for item in cart.values():
            price = float(item['price'].replace('৳', '').replace('Tk', '').strip())
            cart_total += price
            cart_items.append(item)

    context = {
        'cart': cart_items,
        'cart_total': cart_total,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'home/cart.html', context)


def deleteCart(request, pk):
    if request.user.is_authenticated:
        # Existing logic for logged in users
        cart = Cart.objects.get(pk=pk)
        cart.delete()
    else:
        # Handle anonymous users with session
        cart = request.session.get('cart', {})
        if str(pk) in cart:
            del cart[str(pk)]
            request.session['cart'] = cart
            request.session.modified = True
    
    return redirect('cart')


@login_required(login_url='login')
def addWishlist(request, slug):
    product = Product.objects.get(slug=slug)
    wishlist = Wishlist.objects.create(
        product=product,
        host=request.user,
    )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def wishlistPage(request):
    user_id= request.user.pk
    user= User.objects.get(pk=user_id)
    wishlist= user.wishlist_set.all()

    if request.method=="POST":
        wishlist = request.POST.get('w_id')
        product = request.POST.get('p_id')

        whishobj= Wishlist.objects.get(pk=wishlist)
        whishobj.delete()

        return redirect('add_cart', product)

    context={
        'wishlist':wishlist,
    }
    return render(request, 'home/wishlist.html', context)

@login_required(login_url='login')
def deleteWishlist(request,pk):
    wihslist= Wishlist.objects.get(pk=pk)
    wihslist.delete()
    return redirect('wishlist')


def OrderPage(request, slug):
    address = ''
    if request.user.is_authenticated:
        user = request.user
        address = Address.objects.filter(user=user).first()
    product = Product.objects.get(slug=slug)
    
    if request.method == 'POST':
        try:
            order_data = {
                'product': product,
                'size': request.POST.get('size'),
                'quintity': request.POST.get('quintity'),
                'name': request.POST.get('name'),
                'companyname': request.POST.get('company'),
                'country': request.POST.get('country'),
                'home_address': request.POST.get('address'),
                'home_address2': request.POST.get('address2'),
                'town': request.POST.get('town'),
                'postcode': request.POST.get('postcode'),
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
            }

            if request.user.is_authenticated:
                order_data['user'] = request.user

            order = Order.objects.create(**order_data)

            if request.user.is_authenticated and not address:
                Address.objects.create(
                    user=request.user,
                    country=request.POST.get('country'),
                    home_address=request.POST.get('address'),
                    home_address2=request.POST.get('address2'),
                    town=request.POST.get('town'),
                    postcode=request.POST.get('postcode'),
                    phone=request.POST.get('phone'),
                    email=request.POST.get('email')
                )

            try:
                # message sending process start
                name = request.user.name if request.user.is_authenticated else request.POST.get('name')
                subject = f"New Order Received from: {name}"
                dashboard_url = request.build_absolute_uri('/dashboard/orders/')
                messagestr = f"New order received from: {name}\nProduct: {product.taitle}\nView order: {dashboard_url}"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = getattr(settings, 'EMAIL_RECIPIANT')
                send_mail(subject, messagestr, email_from, recipient_list)
            except Exception as e:
                # Log the email error but don't stop the order process
                print(f"Email sending failed: {str(e)}")

            return render(request, 'home/success.html')

        except Exception as e:
            messages.error(request, f"Error creating order: {str(e)}")
            
    context = {
        'product': product,
        'address': address,
    }
    return render(request, 'home/checkout.html', context)    



@login_required(login_url='login')
def cancleOrder(request, pk):
    order= Order.objects.get(pk=pk)

    if order.user != request.user:
        return redirect('home')
    else:
        order.delete()
        return redirect('account')
    # pass


@login_required(login_url='login')
def reveawPage(request, pk):
    user= request.user
    order= Order.objects.get(pk=pk)

    if order.status != 'done':
        return redirect('home')

    if order.user != request.user:
        return redirect('home')

    product= order.product
    a=product.reveaws_set.all().count()
    b= int(a)
    c= int(a+1)

    if request.method=='POST':
        reveaw= Reveaws.objects.create(
                taitle= request.POST.get('taitle'),
                body= request.POST.get('body'),
                product= order.product,
                user= user,
                total= c,
                rating=request.POST.get('rating'),
            )
        order.delete()
        return redirect('account')

    context={}
    return render(request, 'home/reveaw.html', context)
    

def contactPage(request):
    page='contact'
    try:
        if request.method=="POST":
            #message sending process start
            subject = request.POST.get('subject')
            message = request.POST.get('body')
            name= request.POST.get('name')
            email= request.POST.get('email')
            messagestr= "The messege from: "+name+"\n Eamil: "+email+"\n Body: \n"+message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = getattr(settings, 'EMAIL_RECIPIANT')
            send_mail( subject, messagestr, email_from, recipient_list )

            #thanking for the email
            subject = "Thanks for contacting us"
            message = "Hi "+name+", thank you for sending your valuable message. We will reply to you soon."
            email_from = settings.EMAIL_HOST_USER
            recipian= request.POST.get('email')
            recipient_list = [recipian]
            send_mail( subject, message, email_from, recipient_list )

            #if the message sent successfully
            messages.success(request, "Messege has been send successfully!")

            return redirect('contact')
    except :
        messages.error(request, "Sorry we can't sent the messages. Enter valid data and try again!")
    context={
        'page':page,
    }
    return render(request, 'home/contact.html', context)    



def aboutPage(request):
    page="about"
    context={
        'page':page,
    }
    return render(request, 'home/about.html', context)    

def privecyPage(request):
    context={}  
    return render(request, 'home/privecy.html', context)

def termsPage(request):
    context={}
    return render(request, 'home/tearmsandconditions.html', context)


@user_passes_test(lambda u: u.is_superuser)
def mailLatter(request):
    if request.method=="POST":
        subject= request.POST.get('taitle')
        message= request.POST.get('body')
        subscribers= Subscriber.objects.all()

        email_from = settings.EMAIL_HOST_USER
        recipian= request.POST.get('email')
        recipient_list = [subscribers]
        send_mail( subject, message, email_from, recipient_list ) # Order notification

        return redirect('mailsender')

    context={}
    return render(request, 'home/newssender.html', context)


def blogPage(request):
    page = "blog"
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    
    # Base query for published blogs
    blogs = Blog.objects.filter(is_published=True)
    
    # Apply filters based on search and categories/tags
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__name__icontains=q) |
            Q(category__name__icontains=q)
        )
    if category:
        blogs = blogs.filter(category__slug=category)
    if tag:
        blogs = blogs.filter(tags__slug=tag)
        
    blogs = blogs.order_by('-created_date')
    
    # Pagination
    p = Paginator(blogs, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    blog_posts = p.get_page(page_number)
    
    # Sidebar data
    recent_posts = Blog.objects.filter(is_published=True).order_by('-created_date')[:5]
    categories = BlogCategory.objects.all()
    popular_tags = Tag.objects.all()[:10]
    
    context = {
        'page': page,
        'blog_posts': blog_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'popular_tags': popular_tags,
    }
    return render(request, 'home/blog.html', context)


def sellPage(request):
    pagE= "sellp"

    product= Product.objects.annotate(
                    last_review=Max('reveaws__total')
                ).order_by('-last_review')

    p= Paginator(product, 24)
    page= request.GET.get('page')
    productss= p.get_page(page)

    context={
        "page":pagE,
        "products":productss,
    }
    return render(request, 'home/sell.html', context)


def topPage(request):
    pagE= "topp"

    product= Product.objects.annotate(
                    last_review=Max('reveaws__total')
                ).order_by('-last_review')

    p= Paginator(product, 24)
    page= request.GET.get('page')
    productss= p.get_page(page)

    context={
        "page":pagE,
        "products":productss,
    }
    return render(request, 'home/topsell.html', context)

def SeoBarcodeStikerPage(request):

    page= "barcode"
    product= Product.objects.all().filter(catagory__name__icontains="barcode")[0:20]

    context={
        "page":page,
        "products":product,
    }
    return render(request, 'home/seo/barcode-sticker.html', context)

def blogDetailPage(request, slug):
    page = "blog"
    try:
        # Get the blog post and increment view count
        blog = Blog.objects.get(slug=slug, is_published=True)
        blog.views += 1
        blog.save()

        # Get related posts based on category and tags
        related_posts = Blog.objects.filter(
            is_published=True
        ).exclude(
            id=blog.id
        ).filter(
            Q(category=blog.category) | Q(tags__in=blog.tags.all())
        ).distinct()[:3]

        # Handle comments
        if request.method == 'POST' and request.user.is_authenticated:
            content = request.POST.get('content')
            if content:
                BlogComment.objects.create(
                    blog=blog,
                    user=request.user,
                    content=content
                )
                messages.success(request, "Comment submitted successfully and is awaiting approval.")
                return redirect('blog_detail', slug=slug)

        # Get approved comments
        comments = blog.comments.filter(is_approved=True).select_related('user')

        context = {
            'page': page,
            'blog': blog,
            'comments': comments,
            'related_posts': related_posts,
            'total_comments': comments.count(),
        }
        return render(request, 'home/blog-detail.html', context)
    
    except Blog.DoesNotExist:
        messages.error(request, "The blog post you're looking for doesn't exist.")
        return redirect('blog')

def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) >= 2:  # Only return suggestions if query is at least 2 characters
        # Search in product titles and category names
        products = Product.objects.filter(
            Q(taitle__icontains=query) |
            Q(catagory__name__icontains=query)
        ).values('taitle', 'catagory__name')[:5]  # Limit to 5 suggestions
        
        suggestions = []
        for product in products:
            suggestions.append({
                'title': product['taitle'],
                'category': product['catagory__name']
            })
        
        # Add category suggestions
        categories = Catagory.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:3]  # Limit to 3 category suggestions
        
        for category in categories:
            if not any(s.get('category') == category for s in suggestions):
                suggestions.append({
                    'title': f'Category: {category}',
                    'category': category
                })
        
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})


def create_review_link(request):
    if request.method == 'POST':
        review= ProductReview.objects.create(
            customer_name= request.POST.get('name'),
            customer_email= request.POST.get('email'),
            title= request.POST.get('title'),
            review= request.POST.get('review'),
            rating= request.POST.get('rating'),
            images= request.FILES.get('images')
        )
        return render(request, 'home/review_success.html')
    context = {}
    return render(request, 'home/reviews.html', context)

def cart_checkout(request):
    address = ''
    cart_items = []
    cart_total = 0
    
    if request.user.is_authenticated:
        user = request.user
        address = Address.objects.filter(user=user).first()
        cart_items = Cart.objects.filter(host=user)
        cart_total = sum(float(item.product.price.replace('৳', '').replace('Tk', '').strip()) * item.quantity for item in cart_items)
    else:
        cart = request.session.get('cart', {})
        for item_id, item in cart.items():
            product = Product.objects.get(id=item['id'])
            price = float(item['price'].replace('৳', '').replace('Tk', '').strip()) * item['quantity']
            cart_total += price
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'size': item['size'],
                'price': item['price']
            })

    # Default to Dhaka delivery price
    delivery_price = 60
    total = cart_total + delivery_price

    if request.method == 'POST':
        try:
            delivery_location = request.POST.get('delivery_location', 'dhaka')
            delivery_price = 120 if delivery_location == 'outside' else 60
            total = cart_total + delivery_price
            
            # Create the main order
            order = CartOrder.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=request.POST.get('name'),
                country=request.POST.get('country'),
                delivery_location=delivery_location,
                home_address=request.POST.get('address'),
                town=request.POST.get('town'),
                postcode=request.POST.get('postcode'),
                phone=request.POST.get('phone'),
                total_amount=total
            )

            # Send email notification to admin
            try:
                name = request.POST.get('name')
                subject = f"New Cart Order Received from: {name}"
                dashboard_url = request.build_absolute_uri('/dashboard/orders/?type=card')
                messagestr = f"New cart order received from: {name}\nView order: {dashboard_url}"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = getattr(settings, 'EMAIL_RECIPIANT')
                send_mail(subject, messagestr, email_from, recipient_list)
            except Exception as e:
                print(f"Email sending failed: {str(e)}")

            # Create order items
            if request.user.is_authenticated:
                for cart_item in cart_items:
                    CartOrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        size=cart_item.size,
                        price=float(cart_item.product.price.replace('৳', '').replace('Tk', '').strip())
                    )
                cart_items.delete()
            else:
                cart = request.session.get('cart', {})
                for item_id, item in cart.items():
                    product = Product.objects.get(id=item['id'])
                    CartOrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        size=item['size'],
                        price=float(item['price'].replace('৳', '').replace('Tk', '').strip())
                    )
                if 'cart' in request.session:
                    del request.session['cart']
                    request.session.modified = True

            # Save address for logged in users
            if request.user.is_authenticated and not address:
                Address.objects.create(
                    user=request.user,
                    country=request.POST.get('country'),
                    home_address=request.POST.get('address'),
                    home_address2=request.POST.get('address2', ''),
                    town=request.POST.get('town'),
                    postcode=request.POST.get('postcode'),
                    phone=request.POST.get('phone'),
                    email=request.POST.get('email', '')
                )

            return render(request, 'home/success.html')
        except Exception as e:
            messages.error(request, str(e))

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'delivery_price': delivery_price,
        'total': total,
        'address': address,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'home/cart_checkout.html', context)

