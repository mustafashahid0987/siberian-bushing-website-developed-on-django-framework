from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.db.models import Q
import datetime
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
import time
import json
from collections import OrderedDict
from django.contrib import messages  # Import the messages module
from django.http import JsonResponse
import json
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .models import watchlist as w
from django.views import View
import pandas as pd 
import openpyxl
from django.core.files import File





# @login_required(login_url='login')
def index(request):
    products = ProductData.objects.all()
    print(products)
    for i in products:
        print(i.product_category)
    context = {"products":products}
    return render(request,'website/index.html',context)

def about(request):
    return render(request,'website/about-us.html')


def terms(request):
    return render(request,'website/terms.html')

# @login_required(login_url='login')
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email =request.POST.get('email')
        subject =request.POST.get('subject')
        message =request.POST.get('message')
        contact_obj = contact_us.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'you query is received. we will reply you soon.')
        contact_obj.save()

        return redirect('index')
    
    return render(request,'website/contact.html')

def warrenty(request):
    return render(request,'website/warrenty.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print("USER",user)
            if user is not None:
                login(request, user)
                print("LOGGED IN")
                # logout(request)
                messages.success(request, 'you are login sucessfully')
                return redirect('index')
            else:
                print('else chala')
                messages.error(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'website/account-login.html', context)

def logoutP(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        users = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.create_user(username=users, email=email, password=password)
        user_obj.first_name = users
        user_obj.is_superuser = False
        user_obj.save()

        # Add a success message
        messages.success(request, 'Registration successful! You are now logged in.')

        return redirect('login')
        # return render(request,'website/login.html', context)


# @login_required(login_url='login')
def newsletter_sub(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        newsletter_obj = newsletter.objects.create(email=email)
        messages.success(request, 'you have sucessfully subcribed.')
        newsletter_obj.save()

        return redirect('index')

def partnership_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        company = request.POST.get('company')
        staff = request.POST.get('staff')
        website = request.POST.get('website')
        comment = request.POST.get('comment')
        if first_name != None:
            pform_obj = distributor.objects.create(first_name=first_name, lat_name=last_name,
                                                email=email, phone=phone_number, country=country,
                                                company=company,staff=staff, website=website, 
                                                comment=comment)
            messages.success(request, 'Your Distribution Form submitted secessfully.')
            pform_obj.save()

        else:
            return render(request, 'website/partnership.html')

        return redirect('partnership')

    return render(request, 'website/partnership.html')

def SearchDataView(request):
    if request.method == 'POST':
        search_obj = request.POST.get('search')
        products = ProductData.objects.filter(product_title__icontains=search_obj)
        context = {'products':products}
        return render(request, 'website/shop-list.html',context)
    
    return redirect('/')

def product_page_single(request,pk):
    # user_name = request.user.first_name
    product_data = ProductData.objects.filter(id=int(pk))
    
    context = {'product_data':product_data}
    print(product_data) 
    return render(request, 'website/product-full.html', context)


# @login_required(login_url='login')
def add_to_watchlist(request,pk):

    user_id = request.user.id
    # print(pk)
    cc=ProductData.objects.get(id=pk)
    print("coin",cc)
    data=w.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    if not data:
        print("No data")
        obj=w.objects.create(user_id=user_id)
        obj.save()
        obj.coin_ids.add(cc)
        messages.success(request, 'Product is sucessfully added to your wishlist..')
        return redirect('watchlist')
    else:
        print("already")

    return render(request,"website/watchlist")


# @login_required(login_url='login')
def add_to_cart(request,pk):

    user_id = request.user.id
    # print(pk)
    cc=ProductData.objects.get(id=pk)
    print("coin",cc)
    data=addtocart.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    if not data:
        print("No data")
        obj=addtocart.objects.create(user_id=user_id)
        obj.save()
        obj.coin_ids.add(cc)
        messages.success(request, 'Product is sucessfully added to your cart..')
        return redirect('cart')
    else:
        print("already")

    return render(request,'website/cart.html')

# @login_required(login_url='login')
def add_order(request):
    ob = addtocart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        country = request.POST.get('country')
        address = request.POST.get('address')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        confirmation_no = request.POST.get('confirmation_no')
        payment_proof = request.FILES['pf_image']

        discount_obj = request.POST.get('discount_obj')
        print(discount_obj)


        user_id = request.user.id
        print('add order',confirmation_no,payment_proof)


        obj=order.objects.create(user_id=user_id, 
                                country=country,
                                address=address,
                                phone_no=phone_no,
                                email=email,
                                confirmation_no=confirmation_no,
                                payment_proof=payment_proof,
                                status='Pending')
        # obj.save()

        

        for o in range(len(ob)):
            print("add order...",ob[0].coin_ids.all())

            for i in ob[o].coin_ids.all():
                obj1 = ProductData.objects.get(id=i.id)
                obj.coin_ids.add(obj1)

        messages.success(request, 'Your payment is under review..')
        ob.delete()
        
        dis_obj = discount_table.objects.get(id=discount_obj)
        dis_obj.order_limit = 0
        dis_obj.save()
        # cc=ProductData.objects.get(id=pk)
        # print("coin",cc)
        # data=addtocart.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
        # if not data:
        #     print("No data")
        #     obj=order.objects.create(user_id=user_id, 
        #                              confirmation_no=confirmation_no,
        #                              payment_proof=payment_proof,
        #                              status='Pending')
        #     # obj.save()
        #     # obj.coin_ids.add(cc)
        #     messages.success(request, 'Your payment is under review..')
        # else:
        #     print("already")c

        return redirect("my_order")
    
    return redirect('cart')

# @login_required(login_url='login_view')
def watchlist(request):
    ob = w.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []

    for o in range(len(ob)):
        lst1=[]
        print("ss",ob[0].coin_ids.all())
        sign_no.append(o+1)
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            # print("mustafa",obj1)
            lst1.append(obj1)
            lst.append(lst1)

    all_data = zip(sign_no,lst)
    context = {'all_data':all_data}
    return render(request,'website/wishlist.html', context)

# @login_required(login_url='login_view')
def cart(request):

    #code of get data of discount coupon start here..
    try:
        # Retrieve the user based on the user_id
        user = User.objects.get(id=request.user.id)
        print(user)
        # Retrieve the discount_table instance for the user
        discount_instance = discount_table.objects.get(user_ids=user)
        # print('disount coupon',discount_instance)

    except:
        discount_instance = 'none'
        print('you does not have the discount coupon')
    #code of get data of discount coupon ends here...

    ob = addtocart.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []
    subtotal = 0

    for o in range(len(ob)):
        lst1=[]
        sign_no.append(o+1)
        print("ss",ob[0].coin_ids.all())
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            print("mustafa",float(obj1.price_per_pack))
            subtotal += float(obj1.price_per_pack)
            lst1.append(obj1)
            lst.append(lst1)

            # for product in obj1:
            #     subtotal += product.price_per_pack

            

    all_data = zip(sign_no,lst)
    context = {'all_data':all_data,'subtotal':subtotal, 'discount_instance':discount_instance}
    return render(request,'website/cart.html', context)


# @login_required(login_url='login_view')
def remove_watchlist(request,pk):
    print('main hoon',pk, request.user.id)
    obj=w.objects.get(coin_ids=pk, user_id=request.user.id)
    obj.delete()
    print("muti",pk)
    print(obj)
    #return render(request,"coin/watchlist.html")
    return redirect("watchlist")

# @login_required(login_url='login_view')
def remove_cart(request,pk):
    print('main hoon',pk, request.user.id)
    obj=addtocart.objects.get(coin_ids=pk, user_id=request.user.id)
    obj.delete()
    print("muti",pk)
    print(obj)
    #return render(request,"coin/watchlist.html")
    return redirect("cart")

def filter_search(request):
    # context = {'products':products}
    if request.method == 'POST':
        print('if chala')
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')

        data_obj = ProductData.objects.filter(make=make, market=market, model=model, body=body, year=year)
        img_lst = []
        data_lst = []

        print(data_obj)

        for im in data_obj:
            if im.suspension_type == 'Front-Suspension':
                data_lst.append(im)
                img_lst.append(im.search_image_file)

            # if im.suspension_type == 'Rear-Suspension':
            #     data_lst.append(im)
            #     img_lst.append(im.search_image_file)

        try:
            context = {'products':data_lst, 
                    'make':make,
                    'market':market,
                    'model':model,
                    'body':body,
                    'year':year,
                    'img_url':img_lst[0],
                    }
            
        except:
            context = {'products':data_lst, 
                    'make':make,
                    'market':market,
                    'model':model,
                    'body':body,
                    'year':year,
                    'img_url':'None',
                    }
               
        return render(request, 'website/shop-table.html',context)
    
    return render(request, 'website/shop-table.html')


def sema2018(request):
    return render(request,'website/sema2018.html')

def sema2019(request):
    return render(request,'website/sema2019.html')


def initial_data(request):
    # print('working fine...........')


    payload = {'product':['Select Make']}

    make_obj = ProductData.objects.all().distinct()

    for product in make_obj:
        # print(product.make)
        if product.make not in payload['product']:
            payload['product'].append(product.make)

    # print(payload)
    return JsonResponse({'status':200,"data":payload})

def market_filter(request):
    # print('market filter working fine...........')

    selected_make = request.GET.get('name')
    payload = {'market':['Select Market']}
    make_obj = ProductData.objects.filter(make=selected_make)
    
    for ob in make_obj:
        print(ob.market)
        if ob.market not in payload['market']:
            payload['market'].append(ob.market)

    print(payload)
    return JsonResponse({'status':200,"data":payload})


def model_filter(request):
    # print('model filter working fine...........')

    selected_market = request.GET.get('name')
    payload = {'model':['Select Model']}

    make_obj = ProductData.objects.filter(make=selected_market.split(',')[1],market=selected_market.split(',')[0])
    
    for ob in make_obj:
        print(ob.model)
        if ob.model not in payload['model']:
            payload['model'].append(ob.model)

    print(selected_market.split(',')[0],selected_market.split(',')[1])
    return JsonResponse({'status':200,"data":payload})


def body_filter(request):
    # print('body filter working fine...........')

    selected_market = request.GET.get('name')
    payload = {'body':['Select Body']}

    make_obj = ProductData.objects.filter(make=selected_market.split(',')[0],market=selected_market.split(',')[1],model=selected_market.split(',')[2])
    
    for ob in make_obj:
        # print(ob.body)
        if ob.body not in payload['body']:
            payload['body'].append(ob.body)

    # print(selected_market.split(',')[0],selected_market.split(',')[1])
    return JsonResponse({'status':200,"data":payload})


def year_filter(request):
    # print('year filter working fine...........')

    selected_market = request.GET.get('name')
    payload = {'year':['Select Year']}

    make_obj = ProductData.objects.filter(make=selected_market.split(',')[0],market=selected_market.split(',')[1],model=selected_market.split(',')[2],body=selected_market.split(',')[3])
    
    for ob in make_obj:
        # print(ob.year)
        if ob.year not in payload['year']:
            payload['year'].append(ob.year)

    # print(selected_market.split(',')[0],selected_market.split(',')[1])
    return JsonResponse({'status':200,"data":payload})


def suspension_filter(request):
    # print('suspension_filter working fine...........')

    if request.method == 'POST':
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')
        sustype = request.POST.get('sustype')

        print(make,model,year,sustype)

    make_obj = ProductData.objects.filter(make=make,
                                          market=market,
                                          model=model,
                                          body=body,
                                          year=year,
                                         )
    
    print(make_obj)
    data_lst = []
    img_lst = []
    for ob in make_obj:
        print(ob.suspension_type)

        if sustype == 'front':
            if ob.suspension_type == 'Front-Suspension':
                img_lst.append(ob.search_image_file)
                data_lst.append(ob)

        if sustype == 'rear':
            if ob.suspension_type == 'Rear-Suspension':
                img_lst.append(ob.search_image_file)
                data_lst.append(ob)

    try:
        context = {'products':data_lst, 
                'make':make,
                'market':market,
                'model':model,
                'body':body,
                'year':year,
                'img_url':img_lst[0],
                }
    except:
        context = {'products':data_lst, 
                'make':make,
                'market':market,
                'model':model,
                'body':body,
                'year':year,
                'img_url':'None',
                }
                
    
    return render(request, 'website/shop-table.html',context)

def checkout(request):

    if request.method == 'POST':
        selected_payment_method = request.POST.get('pay')
        selected_coupon = request.POST.get('coupon')
        
        try:
            dis_obj = discount_table.objects.get(id=selected_coupon)
        # print('selected coupon: ',dis_obj.discount)
        except:
            dis_obj = 'none'

    if selected_payment_method == 'bank':
        payment_method = 'bank'
        bd_obj = Bank_details.objects.all()
        bd_obj = bd_obj[0]

    elif selected_payment_method == 'zelle':
        payment_method = 'zelle'
        bd_obj = zelle_details.objects.all()
        bd_obj = bd_obj[0]

    ob = addtocart.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []

    for o in range(len(ob)):
        subtotal = 0
        lst1=[]
        sign_no.append(o+1)
        print("ss",ob[0].coin_ids.all())
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            print("mustafa",float(obj1.price_per_pack))
            subtotal += float(obj1.price_per_pack)
            lst1.append(obj1)
            lst.append(lst1)

            # for product in obj1:
            #     subtotal += product.price_per_pack

            
    discounted_price = (float(subtotal) * float(dis_obj.discount)) / 100
    discounted_price = float(subtotal) - float(discounted_price)
    print('subtotal',subtotal)
    print(discounted_price)

    all_data = zip(sign_no,lst)

    context = {'all_data':all_data,
               'subtotal':subtotal,
               'bank_obj':bd_obj,
               'discounted_price':discounted_price,
               'discount_obj':dis_obj,
               'discount_percentage':dis_obj.discount,
               'payment_method':payment_method}

    return render(request, 'website/checkout.html', context)



# @login_required(login_url='login_view')
def my_order(request):
    
    ob = order.objects.filter(user_id=request.user.id)
    print('my order',ob)

    lst=[]
    sign_no = []
    subtotal_lst =[]

    for o in range(len(ob)):
        subtotal = 0
        lst1=[]
        sign_no.append(o+1)
        print("ss",ob[0].coin_ids.all(), ob[o].confirmation_no)
        lst.append(ob)
        
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            print("mustafa",float(obj1.price_per_pack))
            subtotal += float(obj1.price_per_pack)

            # lst1.append(obj1)
            # lst.append(lst1)
        subtotal_lst.append(subtotal)
            # for product in obj1:
            #     subtotal += product.price_per_pack

            
    product = ob
    all_data = zip(sign_no,product,subtotal_lst)
    context = {
                'all_data':all_data,
            #    'subtotal':subtotal,
               }
    return render(request,'website/order_list.html', context)



def order_approval(request,pk):

    obj = order.objects.get(id=pk)
    obj.status = "Approved"
    obj.save()
    messages.success(request, 'The order is approved successfully')
    return redirect("all_orders") 

def order_disapproval(request,pk):

    obj = order.objects.get(id=pk)
    obj.status = "Pending"
    obj.save()
    messages.success(request, 'The order status is changed to pending')
    return redirect("all_orders") 


def all_orders(request):
    order_obj = order.objects.all()
    subtotal_lst = []


    for ord in order_obj:
        subtotal = 0
        # print(ord.coin_ids.all())

        for obj in ord.coin_ids.all():
            # print('cycle')
            # print(obj.price_per_pack)
            subtotal += float(obj.price_per_pack)

        subtotal_lst.append(subtotal)

    print(subtotal_lst)
    all_data = zip(order_obj,subtotal_lst)
    context = {
        'all_data':all_data
    }
    return render(request,'website/all_order.html',context)


def order_detail(request,pk):
    obj = order.objects.get(id=pk)
    user_obj = User.objects.get(id=obj.user_id)
    # print(user_obj.username)

    product_lst = []
    subtotal = 0
    for product in obj.coin_ids.all():

        product_lst.append(product)
        subtotal += float(product.price_per_pack)

    print('payment proof is here...',obj.payment_proof)
    context={
        'obj':obj,
        'product_lst':product_lst,
        'subtotal':subtotal,
        'user_obj':user_obj,
    }
    return render(request,'website/order-details.html',context)



def all_products(request):
    product_obj = ProductData.objects.all()
    sn_lst = []


    for sn in range(len(product_obj)):
        sn_lst.append(sn+1)

    print(sn_lst)
    all_data = zip(product_obj,sn_lst)
    context = {
        'all_data':all_data
    }
    return render(request,'website/all_products.html',context)

# @login_required(login_url='login_view')
def remove_product(request,pk):
    print('main hoon',pk, request.user.id)
    obj=ProductData.objects.get(id=pk)
    obj.delete()
    print("muti",pk)
    print(obj)
    # return render(request,"website/all_products.html")
    return redirect("all_products")


def add_product(request):

    if request.method == 'POST':
        model = request.POST.get('model_no')
        bushing_no = request.POST.get('bushing_no')
        title = request.POST.get('title')
        descripiton = request.POST.get('descripiton')
        weight = request.POST.get('weight')
        package = request.POST.get('package')
        ppp = request.POST.get('ppp')
        ppu = request.POST.get('ppu')
        pimage = request.POST.get('pimage')
        simage = request.POST.get('simage')
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')
        status = request.POST.get('status')
        select_type = request.POST.get('st')
        select_category = request.POST.get('sc')

        prod_obj = ProductData.objects.create(model_no=model,
                                              bushing_no=bushing_no,
                                            product_title = title,
                                            product_description = descripiton,
                                            weight = weight,
                                            package = package,
                                            price_per_pack = ppp,
                                            price_per_unit = ppu,
                                            image_file = pimage,
                                            search_image_file = simage,
                                            make = make,
                                            market = market,
                                            model = model,
                                            body = body,
                                            year = year,
                                            status=status,
                                            suspension_type = select_type,
                                            product_category = select_category
                                            )
        
        prod_obj.save()
        messages.success(request, 'The product is added sucessfully')

        return redirect('all_products')


    return render(request,'website/add_product.html')


def add_bulk_product(request):

    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        # Read the Excel file-no into a DataFrame
        df = pd.read_excel(excel_file,engine='openpyxl')
        model_lst = df['model_no'].tolist()
        bushing_lst = df['bushing_no'].tolist()
        title_lst = df['title'].tolist()
        description_lst = df['description'].tolist()
        weight_lst = df['weight'].tolist()
        package_lst = df['package'].tolist()
        ppp_lst = df['price_per_pack'].tolist()
        ppu_lst = df['price_per_unit'].tolist()
        image_file_lst = df['image_file'].tolist()
        search_image_file_lst = df['search_image_file'].tolist()
        make = df['make'].tolist()
        market = df['market'].tolist()
        model = df['model'].tolist()
        body = df['body'].tolist()
        year = df['year'].tolist()
        status = df['status'].tolist()
        suspension_type = df['suspension_type'].tolist()
        product_category = df['product_category'].tolist()
        

        print(image_file_lst[0].split('\\')[-1])

        # for row in sheet.iter_rows(min_row=2, values_only=True):
        #     print(row['Ticker'])

        for i in range(len(model_lst)):

            prod_obj = ProductData.objects.create(model_no=model_lst[i],
                                                bushing_no=bushing_lst[i],
                                                product_title = title_lst[i],
                                                product_description = description_lst[i],
                                                weight = weight_lst[i],
                                                package = package_lst[i],
                                                price_per_pack = ppp_lst[i],
                                                price_per_unit = ppu_lst[i],
                                                # image_file = image_file[0],
                                                # search_image_file = search_image_file[0],
                                                make = make[i],
                                                market = market[i],
                                                model = model[i],
                                                body = body[i],
                                                year = year[i],
                                                status=status[i],
                                                suspension_type = suspension_type[i],
                                                product_category = product_category[i]
                                                )
            
            # prod_obj.save()

            image_path = image_file_lst[i]
            with open(image_path, "rb") as image_file:
                image_name = image_path.split("\\")[-1]  # Extract the image file name from the path
                your_model_instance = ProductData.objects.last()  # Retrieve the instance you want to associate with the image

                # Assign the image to the model field (e.g., 'image_field_name')
                your_model_instance.image_file.save(image_name, File(image_file))

            image_path = search_image_file_lst[i]
            with open(image_path, "rb") as image_file:
                image_name = image_path.split("\\")[-1]  # Extract the image file name from the path
                your_model_instance = ProductData.objects.last()  # Retrieve the instance you want to associate with the image

                # Assign the image to the model field (e.g., 'image_field_name')
                your_model_instance.search_image_file.save(image_name, File(image_file))


        messages.success(request, 'The product is added sucessfully')

    return redirect('all_products')


def update_product(request,pk):

    print('product id',pk)
    prod_obj = ProductData.objects.get(id=pk)

    if request.method == 'POST':
        model = request.POST.get('model_no')
        bushing_no = request.POST.get('bushing_no')
        title = request.POST.get('title')
        descripiton = request.POST.get('description')
        weight = request.POST.get('weight')
        package = request.POST.get('package')
        ppp = request.POST.get('ppp')
        ppu = request.POST.get('ppu')
        pimage = request.POST.get('pimage')
        simage = request.POST.get('simage')
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')
        status = request.POST.get('status')
        select_type = request.POST.get('st')
        select_category = request.POST.get('sc')

        
        prod_obj.model_no=model,
        prod_obj.bushing_no=bushing_no,
        prod_obj.product_title = title
        prod_obj.product_description = descripiton
        prod_obj.weight = weight
        prod_obj.package = package
        prod_obj.price_per_pack = ppp
        prod_obj.price_per_unit = ppu
        if pimage != '':
            prod_obj.image_file = pimage
        if simage != '':
            prod_obj.search_image_file = simage
        prod_obj.make = make
        prod_obj.market = market
        prod_obj.model = model
        prod_obj.body = body
        prod_obj.year = year
        prod_obj.status = status
        prod_obj.suspension_type = select_type
        prod_obj.product_category = select_category
        prod_obj.save()                                    
        
        messages.success(request, 'The product is updated sucessfully')

        return redirect('all_products')

    context = {'product_obj':prod_obj}
    return render(request,'website/update_product.html',context)


def copy_product(request,pk):
    print('product id',pk)
    prod_obj = ProductData.objects.get(id=pk)

    if request.method == 'POST':
        model = request.POST.get('model_no')
        bushing_no = request.POST.get('model_no')
        title = request.POST.get('title')
        descripiton = request.POST.get('description')
        weight = request.POST.get('weight')
        package = request.POST.get('package')
        ppp = request.POST.get('ppp')
        ppu = request.POST.get('ppu')
        pimage = request.POST.get('pimage')
        simage = request.POST.get('simage')
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')
        status = request.POST.get('status')
        select_type = request.POST.get('st')
        select_category = request.POST.get('sc')

        if pimage == '':
            pimage = prod_obj.image_file

        if simage == '':
            simage = prod_obj.search_image_file

        prod_obj = ProductData.objects.create(model_no=model,
                                              bushing_no=bushing_no,
                                            product_title = title,
                                            product_description = descripiton,
                                            weight = weight,
                                            package = package,
                                            price_per_pack = ppp,
                                            price_per_unit = ppu,
                                            image_file = pimage,
                                            search_image_file = simage,
                                            make = make,
                                            market = market,
                                            model = model,
                                            body = body,
                                            year = year,
                                            status=status,
                                            suspension_type = select_type,
                                            product_category = select_category
                                            )
        
        prod_obj.save()
        messages.success(request, 'The product is added sucessfully')

        return redirect('all_products')

    context = {'product_obj':prod_obj}
    return render(request,'website/update_product.html',context)

def dashboard(request):
    prod_obj = ProductData.objects.all()
    order_obj = order.objects.all()
    user_obj = User.objects.all()
    approve_orders = 0

    for ord in order_obj:
        if ord.status == 'Approved':
            approve_orders += 1


    context = {
        'products':len(prod_obj),
        'orders':len(order_obj),
        'users':len(user_obj),
        'approved_orders':approve_orders
    }

    return render(request,'website/dashboard.html',context)


def all_contacts(request):

    contact_obj = contact_us.objects.all()
    sn_lst = []

    for i in range(len(contact_obj)):
        sn_lst.append(i+1)

    all_data = zip(contact_obj, sn_lst)

    context={
        'all_data':all_data
    }

    return render(request,'website/all_contact_forms.html',context)


def all_distributors(request):

    dis_obj = distributor.objects.all()
    sn_lst = []

    for i in range(len(dis_obj)):
        sn_lst.append(i+1)

    all_data = zip(dis_obj, sn_lst)

    context={
        'all_data':all_data
    }

    return render(request,'website/all_distributors.html',context)


def view_distributor(request, pk):
    dis_obj = distributor.objects.get(id=pk)
    print('dis onbjecct',dis_obj)
    context = {'dis_obj':dis_obj,}

    return render(request,'website/view_distributor.html',context)


def all_users(request):

    user_obj = User.objects.all()
    sn_lst = []

    for i in range(len(user_obj)):
        sn_lst.append(i+1)

    all_data = zip(user_obj, sn_lst)

    context={
        'all_data':all_data
    }

    return render(request,'website/all_users.html',context)


def view_user(request, pk):
    print(pk)

    user_obj = User.objects.get(id=pk)

    ob = w.objects.filter(user_id=pk)
    print(ob)

    lst=[]
    sign_no = []

    for o in range(len(ob)):
        lst1=[]
        print("ss",ob[0].coin_ids.all())
        sign_no.append(o+1)
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            # print("mustafa",obj1)
            lst1.append(obj1)
            lst.append(lst1)

    wish_data = zip(sign_no,lst)


    order_ob = order.objects.filter(user_id=pk)
    print('my order',order_ob)

    lst=[]
    sign_no = []


    for o in range(len(order_ob)):
        lst1=[]
        sign_no.append(o+1)
        print("ss",order_ob[0].coin_ids.all(), order_ob[o].confirmation_no)
        lst.append(order_ob)
        

            
    product = order_ob
    order_data = zip(sign_no,product)


    context = {
        'user_obj':user_obj,
        'wish_data':wish_data,
        'order_data':order_data
        }

    return render(request,'website/view_user.html',context)


def all_discount(request):
    discount_obj = discount_table.objects.all()
    sn_lst = []


    for sn in range(len(discount_obj)):
        sn_lst.append(sn+1)

    # print(discount_obj[0].discount)
    all_data = zip(discount_obj,sn_lst)

    context = {
        'all_data':all_data
    }
    return render(request,'website/all_discount.html',context)


def give_discount(request):
    user_obj = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        discount = request.POST.get('discount')
        order_limit = request.POST.get('order_limit')

        # obj1 = User.objects.get(id=user_id)

        # print(user_id, discount, order_limit)

        # uobj = discount_table.objects.create(
        #     discount = discount,
        #     order_limit = order_limit
        # )


        # uobj.save()
        # uobj.user_ids.add(obj1)

        # Retrieve the user based on the user_id
        user = User.objects.get(id=user_id)

        # Create or get the discount_table instance for the user
        discount_instance, created = discount_table.objects.get_or_create(user_ids=user)

        # Update the fields
        discount_instance.discount = discount
        discount_instance.order_limit = order_limit

        # Save the changes
        discount_instance.save()


        messages.success(request, 'The coupon is sucessfully send to' + str(user_id))

        return redirect('all_discount')


    context = {
        'user_obj':user_obj
    }

    return render(request,'website/give_discount.html',context)



def update_coupon(request,pk):

    discount_obj = discount_table.objects.get(id=pk)

    if request.method == 'POST':
        # user_id = request.POST.get('user')
        discount = request.POST.get('discount')
        order_limit = request.POST.get('order_limit')


    #     user_obj = User.objects.get(id=user_id)

    #     discount_obj.user_ids=user_obj,
        discount_obj.discount=discount
        discount_obj.order_limit = order_limit

        discount_obj.save()      
        
        messages.success(request, 'The coupon is updated sucessfully')

        return redirect('all_discount')

    context = {'discount_obj':discount_obj}
    return render(request,'website/update_coupon.html',context)


# @login_required(login_url='login_view')
def remove_coupon(request,pk):
    print('main hoon',pk, request.user.id)
    obj=discount_table.objects.get(id=pk)
    obj.delete()
    print("muti",pk)
    print(obj)
    # return render(request,"website/all_products.html")
    return redirect("all_discount")