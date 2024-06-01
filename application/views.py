import random

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse

from .forms import User_RegForm, Farmer_RegForm, FarmHouse_RegForm, LoginForm, Add_CategoryForm, Edit_CategoryForm, \
    Edit_UserProfile_Form, Edit_FarmerProfile_Form, Edit_FarmHouseProfile_Form, Add_ProductsForm \
    , Edit_ProductsForm, addDeliveryAgentForm, add_policyform, edit_policyform, edit_agentform, add_catform, \
    edit_categoryForm, add_tipsform, edit_tipsform, edit_machine_categoryform, add_machine_categoryform, \
    add_machineryform, edit_machineryform, Request_form
from .models import User_Reg, Farmer_Reg, FarmHouse_Reg, Category, Product, cart, cart_items, delivery_agent, orders, \
    govt_policies \
    , tip_category, tips, rental_product, rental_category, rental_request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import logout as logouts
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def about(request):
    return render(request, 'temp/about.html')


def blog(request):
    return render(request, 'temp/blog.html')


def index(request):
    return render(request, 'temp/index.html')


def blog_single(request):
    return render(request, 'temp/blog-single.html')


def Cart(request):
    return render(request, 'temp/cart.html')


def Checkout(request):
    return render(request, 'temp/checkout.html')


def contact(request):
    return render(request, 'temp/contact.html')


def product_single(request):
    return render(request, 'temp/product-single.html')


def shop(request):
    return render(request, 'temp/shop.html')


def wishlist(request):
    return render(request, 'temp/wishlist.html')


def User_Register(request):
    if request.method == 'POST':
        form = User_RegForm(request.POST)
        if form.is_valid():
            email_val = form.cleaned_data['Email']
            if User.objects.filter(email=email_val).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/User_Register/')
            else:
                form.save()
                uname = User_Reg.objects.get(Email=email_val)
                User.objects.create_user(username=uname, email=email_val)
                # fname = form.cleaned_data['firstname']
                # lname = form.cleaned_data['lastname']
                # subject = 'welcome to GFG world'
                # message = f'Hi {fname} {lname}, thank you for registering in geeksforgeeks.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['aiswaryam421@gmail.com', ]
                # send_mail(subject, message, email_from, recipient_list)
                messages.warning(request, "Registration Successful")
                return redirect('/User_Register/')

    else:
        form_value = User_RegForm()
        return render(request, "User/User_Register.html", {'form_key': form_value})


def Farmer_Register(request):
    if request.method == 'POST':
        form = Farmer_RegForm(request.POST, request.FILES)
        if form.is_valid():
            email_val = form.cleaned_data['Email']
            if User.objects.filter(email=email_val).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/Farmer_Register/')
            else:
                form.save()
                uname = Farmer_Reg.objects.get(Email=email_val)
                User.objects.create_user(username=uname, email=email_val)
                # fname = form.cleaned_data['firstname']
                # lname = form.cleaned_data['lastname']
                # subject = 'welcome to GFG world'
                # message = f'Hi {fname} {lname}, thank you for registering in geeksforgeeks.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['aiswaryam421@gmail.com', ]
                # send_mail(subject, message, email_from, recipient_list)
                messages.warning(request, "Registration Successful")
                return redirect('/Farmer_Register/')

    else:
        form_value = Farmer_RegForm()
        return render(request, "Farmer/Farmer_Register.html", {'form_key': form_value})


def FarmHouse_Register(request):
    if request.method == 'POST':
        form = FarmHouse_RegForm(request.POST, request.FILES)
        if form.is_valid():
            email_val = form.cleaned_data['Email']
            if User.objects.filter(email=email_val).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/FarmHouse_Register/')
            else:
                form.save()
                uname = FarmHouse_Reg.objects.get(Email=email_val)
                User.objects.create_user(username=uname, email=email_val)
                # fname = form.cleaned_data['firstname']
                # lname = form.cleaned_data['lastname']
                # subject = 'welcome to GFG world'
                # message = f'Hi {fname} {lname}, thank you for registering in geeksforgeeks.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['aiswaryam421@gmail.com', ]
                # send_mail(subject, message, email_from, recipient_list)
                messages.warning(request, "Registration Successful")
                return redirect('/FarmHouse_Register/')

    else:
        form_value = FarmHouse_RegForm()
        return render(request, "FarmHouse/FarmHouse_Register.html", {'form_key': form_value})


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email_val = form.cleaned_data['Email']
            pswd = form.cleaned_data['Password']
            try:
                user = User_Reg.objects.get(Email=email_val)
                if user:
                    try:
                        user1 = User_Reg.objects.get(Q(User_Id=user.User_Id) & Q(Password=pswd))
                        if user1:
                            request.session['session_id'] = user.User_Id
                            if user.User_Type == 1:
                                return redirect('/Admin_Home/%s' % user.User_Id)
                            else:
                                return redirect('/User_Home/%s' % user.User_Id)
                    except User_Reg.DoesNotExist:
                        user1 = None
                        messages.warning(request, "Incorrect Password")
                        return redirect('/Login/')
            except User_Reg.DoesNotExist:
                try:
                    user = Farmer_Reg.objects.get(Email=email_val)
                    if user:
                        try:
                            user1 = Farmer_Reg.objects.get(Q(Farmer_Id=user.Farmer_Id) & Q(Password=pswd))
                            if user1:
                                if user.Status == True:
                                    request.session['session_id'] = user.Farmer_Id
                                    return redirect('/Farmer_Home/%s' % user.Farmer_Id)
                                else:
                                    return redirect('/Login/')
                        except Farmer_Reg.DoesNotExist:
                            user1 = None
                            messages.warning(request, "Incorrect Password")
                            return redirect('/Login/')
                except Farmer_Reg.DoesNotExist:
                    try:
                        user = FarmHouse_Reg.objects.get(Email=email_val)
                        if user:
                            try:
                                user1 = FarmHouse_Reg.objects.get(Q(FarmHouse_Id=user.FarmHouse_Id) & Q(Password=pswd))
                                if user1:
                                    if user.Status == True:
                                        request.session['session_id'] = user.FarmHouse_Id
                                        return redirect('/FarmHouse_Home/%s' % user.FarmHouse_Id)
                                    else:
                                        return redirect('/Login/')
                            except FarmHouse_Reg.DoesNotExist:
                                user1 = None
                                messages.warning(request, "Incorrect Password")
                                return redirect('/Login/')
                    except FarmHouse_Reg.DoesNotExist:
                        try:
                            user = delivery_agent.objects.get(email=email_val)
                            if user:
                                try:
                                    user1 = delivery_agent.objects.get(
                                        Q(agent_id=user.agent_id) & Q(password=pswd))
                                    if user1:
                                        if user.usertype == 5:
                                            request.session['session_id'] = user.agent_id
                                            return redirect('/delivery_agent_home/%s' % user.agent_id)
                                        else:
                                            return redirect('/Login/')
                                except delivery_agent.DoesNotExist:
                                    user1 = None
                                    messages.warning(request, "Incorrect Password")
                                    return redirect('/Login/')
                        except delivery_agent.DoesNotExist:
                            user = None
                            messages.warning(request, "Invalid Email Id")
                            return redirect('/Login/')
    else:
        form1 = LoginForm()
        return render(request, "login.html", {'form': form1})


def Farmer_Home(request, uid):
    category = get_rentalcategory()
    return render(request, 'Farmer/Farmer_Home.html', {'login_id': uid, 'category': category})


def User_Home(request, uid):
    if request.session.get('session_id'):
        categories = get_category()
        return render(request, "User/User_Home.html", {'login_id': uid, 'categories': categories})
    else:
        return redirect('/Login/')


def FarmHouse_Home(request, uid):
    return render(request, 'FarmHouse/FarmHouse_Home.html', {'login_id': uid})


def Farmer_Table(request, uid):
    if request.session.get('session_id'):
        farmer = Farmer_Reg.objects.filter(Status=False)
        return render(request, 'Farmer/Farmer_Table.html', {'login_id': uid, 'farmer': farmer})
    else:
        return redirect('/Login/')


def FarmHouse_Table(request, uid):
    if request.session.get('session_id'):
        farmhouse = FarmHouse_Reg.objects.filter(Status=False)
        return render(request, 'FarmHouse/FarmHouse_Table.html', {'login_id': uid, 'farmhouse': farmhouse})
    else:
        return redirect('/Login/')


def Admin_Home(request, uid):
    if request.session.get('session_id'):
        return render(request, 'Admin/Admin_Home.html', {'login_id': uid})
    else:
        return redirect('/Login/')


def Approve_Farmer(request, uid, id):
    if request.session.get('session_id'):
        Farmer_Reg.objects.filter(Farmer_Id=id).update(Status=True)
        return redirect('/Farmer_Table/%s' % uid)
    else:
        return redirect('/Login/')


def Reject_Farmer(request, uid, id):
    if request.session.get('session_id'):
        farmer = Farmer_Reg.objects.get(Farmer_Id=id)
        user = User.objects.get(email=farmer.Email)
        user.delete()
        reject = Farmer_Reg.objects.filter(Farmer_Id=id).delete()
        return redirect('/Farmer_Table/%s' % uid)
    else:
        return redirect('/Login/')


def Approve_FarmHouse(request, uid, id):
    if request.session.get('session_id'):
        FarmHouse_Reg.objects.filter(FarmHouse_Id=id).update(Status=True)
        return redirect('/FarmHouse_Table/%s' % uid)
    else:
        return redirect('/Login/')


def Reject_FarmHouse(request, uid, id):
    if request.session.get('session_id'):
        farmhouse = FarmHouse_Reg.objects.get(FarmHouse_Id=id)
        user = User.objects.get(email=farmhouse.Email)
        user.delete()
        reject = FarmHouse_Reg.objects.filter(FarmHouse_Id=id).delete()
        return redirect('/FarmHouse_Table/%s' % uid)
    else:
        return redirect('/Login/')


def List_Farmer(request, uid):
    if request.session.get('session_id'):
        farmer = Farmer_Reg.objects.filter(Status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(farmer, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'Farmer/List_Farmer.html', {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def List_FarmHouse(request, uid):
    if request.session.get('session_id'):
        farmhouse = FarmHouse_Reg.objects.filter(Status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(farmhouse, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'FarmHouse/List_FarmHouse.html', {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def List_User(request, uid):
    if request.session.get('session_id'):
        User = User_Reg.objects.filter(User_Type=2)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(User, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'User/List_User.html', {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def Delete_Farmer(request, uid, id):
    if request.session.get('session_id'):
        farmer = Farmer_Reg.objects.get(Farmer_Id=id)
        user = User.objects.get(email=farmer.Email)
        user.delete()
        Farmer_Reg.objects.filter(Farmer_Id=id).delete()
        return redirect('/List_Farmer/%s' % uid)
    else:
        return redirect('/Login/')


def Delete_FarmHouse(request, uid, id):
    if request.session.get('session_id'):
        farmhouse = FarmHouse_Reg.objects.get(FarmHouse_Id=id)
        user = User.objects.get(email=farmhouse.Email)
        user.delete()
        FarmHouse_Reg.objects.filter(FarmHouse_Id=id).delete()
        return redirect('/List_FarmHouse/%s' % uid)
    else:
        return redirect('/Login/')


def Delete_User(request, uid, id):
    if request.session.get('session_id'):
        user1 = User_Reg.objects.get(User_Id=id)
        user = User.objects.get(email=user1.Email)
        user.delete()
        User_Reg.objects.filter(User_Id=id).delete()
        return redirect('/List_User/%s' % uid)
    else:
        return redirect('/Login/')


def Add_Category(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = Add_CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, "Category Added Successfully")
                return redirect('/Add_Category/%s' % uid)
        else:
            form_value = Add_CategoryForm()
            return render(request, "Admin/Add_Category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def Edit_Category(request, uid, id):
    if request.session.get('session_id'):
        categories = Category.objects.get(Category_Id=id)
        if request.method == 'POST':
            form = Edit_CategoryForm(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/List_Category/%s' % uid)
        else:
            form_value = Edit_CategoryForm(instance=categories)
            return render(request, "Admin/Edit_Category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def List_Category(request, uid):
    if request.session.get('session_id'):
        categories = Category.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Admin/List_Category.html",
                      {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def Delete_Category(request, uid, id):
    if request.session.get('session_id'):
        Category.objects.get(Category_Id=id).delete()
        return redirect('/List_Category/%s' % uid)
    else:
        return redirect('/Login/')


def logout(request):
    del request.session['session_id']
    logouts(request)
    return redirect('/')


def User_Profile(request, uid):
    if request.session.get('session_id'):
        user = User_Reg.objects.get(User_Id=uid)
        return render(request, "User/User_Profile.html", {'user': user, 'login_id': uid})
    else:
        return redirect('/Login/')


def Edit_UserProfile(request, uid):
    if request.session.get('session_id'):
        user = User_Reg.objects.get(User_Id=uid)
        if request.method == 'POST':
            form = Edit_UserProfile_Form(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/User_Profile/%s' % uid)

        else:
            form_value = Edit_UserProfile_Form(instance=user)
            return render(request, "User/Edit_UserProfile.html",
                          {'form_key': form_value, 'user': user, 'login_id': uid})
    else:
        return redirect('/Login/')


def Farmer_Profile(request, uid):
    if request.session.get('session_id'):
        farmer = Farmer_Reg.objects.get(Farmer_Id=uid)
        return render(request, "Farmer/Farmer_Profile.html", {'farmer': farmer, 'login_id': uid})
    else:
        return redirect('/Login/')


def Edit_FarmerProfile(request, uid):
    if request.session.get('session_id'):
        farmer = Farmer_Reg.objects.get(Farmer_Id=uid)
        if request.method == 'POST':
            form = Edit_FarmerProfile_Form(request.POST, instance=farmer)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/Farmer_Profile/%s' % uid)

        else:
            form_value = Edit_FarmerProfile_Form(instance=farmer)
            return render(request, "Farmer/Edit_FarmerProfile.html",
                          {'form_key': form_value, 'farmer': farmer, 'login_id': uid})
    else:
        return redirect('/Login/')


def FarmHouse_Profile(request, uid):
    if request.session.get('session_id'):
        farmhouse = FarmHouse_Reg.objects.get(FarmHouse_Id=uid)
        return render(request, "FarmHouse/FarmHouse_Profile.html", {'farmhouse': farmhouse, 'login_id': uid})
    else:
        return redirect('/Login/')


def Edit_FarmHouseProfile(request, uid):
    if request.session.get('session_id'):
        farmhouse = FarmHouse_Reg.objects.get(FarmHouse_Id=uid)
        if request.method == 'POST':
            form = Edit_FarmHouseProfile_Form(request.POST, instance=farmhouse)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/FarmHouse_Profile/%s' % uid)

        else:
            form_value = Edit_FarmHouseProfile_Form(instance=farmhouse)
            return render(request, "FarmHouse/Edit_FarmHouseProfile.html",
                          {'form_key': form_value, 'farmhouse': farmhouse, 'login_id': uid})
    else:
        return redirect('/Login/')


def Add_Product(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = Add_ProductsForm(request.POST, request.FILES)
            if form.is_valid():
                categories = form.cleaned_data['Categories']
                name = form.cleaned_data['Name']
                description = form.cleaned_data['Description']
                price = form.cleaned_data['Price']
                image = form.files['Image']
                farmer_id = Farmer_Reg.objects.get(Farmer_Id=uid)
                Product.objects.create(Categories=categories, Name=name, Description=description, Price=price,
                                       Image=image,
                                       Farmer_Id=farmer_id)
                messages.warning(request, "Product Added Successfully")
                return redirect('/Add_Product/%s' % uid)
        else:
            form_value = Add_ProductsForm()
            return render(request, "Product/Add_Product.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def Edit_Product(request, uid, id):
    if request.session.get('session_id'):
        products = Product.objects.get(Product_Id=id)
        if request.method == 'POST':
            form = Edit_ProductsForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/Product_List/%s' % uid)
        else:
            form_value = Edit_ProductsForm(instance=products)
            return render(request, "Product/Edit_Product.html",
                          {'form_key': form_value, 'products': products, 'login_id': uid})
    else:
        return redirect('/Login/')


def Product_List(request, uid):
    if request.session.get('session_id'):
        products = Product.objects.filter(Farmer_Id=uid)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Product/Product_List.html",
                      {'products': products, 'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/Login/')


def Delete_Product(request, uid, id):
    if request.session.get('session_id'):
        Product.objects.get(Product_Id=id).delete()
        return redirect('/Product_List/%s' % uid)
    else:
        return redirect('/Login/')


def Admin_Delete_Product(request, uid, id):
    if request.session.get('session_id'):
        Product.objects.get(Product_Id=id).delete()
        return redirect('/Product_List/%s' % uid)
    else:
        return redirect('/Login/')


def Admin_Product_List(request, uid):
    if request.session.get('session_id'):
        products = Product.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Admin/Product_List.html", {'products': products, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def get_products(request, uid, id):
    if request.session.get('session_id'):
        products = Product.objects.filter(Categories=id)
        categories = get_category()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 8)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "User/view_products.html",
                      {'page_obj': page_obj, 'login_id': uid, 'categories': categories})
    else:
        return redirect('/Login/')


def delivery_agent_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "delivery/delivery_agent_home.html", {'login_id': uid})
    else:
        return redirect('/Login/')


def delivery_agent_list(request, uid):
    if request.session.get('session_id'):
        agent = delivery_agent.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(agent, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        return render(request, "Admin/delivery_agent_list.html",
                      {'agents': agent, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def delete_delivery_agent(request, uid, id):
    if request.session.get('session_id'):
        delivery_agent.objects.get(agent_id=id).delete()
        return redirect('/delivery_agent_list/%s' % uid)
    else:
        return redirect('/Login/')


def delivery_agent_reg(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = addDeliveryAgentForm(request.POST, request.FILES)
            length_of_string = 10
            sample_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@$^&*/!"
            pswd = ''.join(random.choices(sample_str, k=length_of_string))
            if form.is_valid():
                name = form.cleaned_data['name']
                post_email = form.cleaned_data['email']
                id_proof = form.files['id_proof']
                if User.objects.filter(email=post_email).exists():
                    messages.warning(request, "Email Id Already Exist")
                    return redirect('/delivery_agent_reg/%s' % uid)
                else:
                    delivery_agent.objects.create(name=name, email=post_email, password=pswd, id_proof=id_proof)
                    uname = delivery_agent.objects.get(email=post_email)
                    User.objects.create_user(username=uname, email=post_email)
                    name = form.cleaned_data['name']
                    # subject = 'Welcome to Organic Store'
                    # message = f'Hi {name}, Thank you for accepting our invitaion to join Organic Store.\n' \
                    #           f'Your Email Id and Password has been provided below :\n' \
                    #           f'Email Id : {post_email} \n' \
                    #           f'Password : {pswd} \n' \
                    #           f'Thank you..'
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = ['', ]
                    # send_mail(subject, message, email_from, recipient_list)
                    # messages.warning(request, "Registration Successful")
                    return redirect('/delivery_agent_reg/%s' % uid)
        else:
            form_value = addDeliveryAgentForm()
            return render(request, "Admin/add_delivery_agent.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def get_category():
    categories = Category.objects.all()
    return categories


def add_to_cart(request, uid, products_id):
    if request.session.get('session_id'):
        products = Product.objects.get(Product_Id=products_id)
        customers = User_Reg.objects.get(User_Id=uid)
        condition1 = Q(user_id=uid)
        condition2 = Q(status=True)
        try:
            carts = cart.objects.get(condition1 & condition2)

            if carts:
                cart_item = cart_items.objects.create(product_id=products, carts_id=carts, user_id=customers,
                                                      farmers_id=products.Farmer_Id)
                count = carts.count + 1
                cart.objects.filter(user_id=uid).update(count=count)
                print(count)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            carts = cart.objects.create(user_id=customers, count=1)
            cart_item = cart_items.objects.create(product_id=products, carts_id=carts, user_id=customers,
                                                  farmers_id=products.Farmer_Id)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/Login/')


def carts(request, uid):
    if request.session.get('session_id'):
        categories = get_category()
        condition1 = Q(user_id=uid)
        condition2 = Q(status=True)
        try:
            carts = cart.objects.get(condition1 & condition2)
            try:
                cart_item = cart_items.objects.get(carts_id=carts.cart_id)
                return render(request, "cart/cart.html",
                              {'cart_item': cart_item, 'login_id': uid, 'categories': categories, 'count': carts.count,
                               'cart_id': carts.cart_id})
            except cart_items.DoesNotExist:
                messages.warning(request, "Your cart is Empty")
                return render(request, "cart/cart.html", {'login_id': uid, 'categories': categories})
            except cart_items.MultipleObjectsReturned:
                cart_item = cart_items.objects.filter(carts_id=carts.cart_id)
                return render(request, "cart/cart.html",
                              {'cart_item': cart_item, 'login_id': uid, 'categories': categories, 'count': carts.count,
                               'cart_id': carts.cart_id})
        except cart.DoesNotExist:
            messages.warning(request, "Your cart is Empty")
            return render(request, "cart/cart.html", {'login_id': uid, 'categories': categories})
    else:
        return redirect('/Login/')


def remove_cart_item(request, uid, id, cart_id):
    if request.session.get('session_id'):
        cart_items.objects.get(item_id=id).delete()
        carts = cart.objects.get(cart_id=cart_id)
        count = carts.count - 1
        cart.objects.filter(cart_id=cart_id).update(count=count)
        return redirect('/carts/%s' % uid)
    else:
        return redirect('/Login/')


def get_item_count(request):
    if request.session.get('session_id'):
        uid = request.GET.get('login_id')
        condition1 = Q(user_id=uid)
        condition2 = Q(status=True)
        try:
            carts = cart.objects.get(condition1 and condition2)
            data = {'status': True, 'count': carts.count}
            return JsonResponse(data)
        except cart.DoesNotExist:
            data = {'status': False, 'count': 0}
            return JsonResponse(data)
    else:
        return redirect('/Login/')


def inc_qty(request, uid, item_id):
    if request.session.get('session_id'):
        try:
            cart_item = cart_items.objects.get(item_id=item_id)
            if cart_item.qty < 5:
                qty = cart_item.qty + 1
            else:
                qty = 5
            cart_item1 = cart_items.objects.filter(item_id=item_id).update(qty=qty)
            return redirect('/carts/%s' % uid)
        except cart_items.DoesNotExist:
            cart_item = None
            return redirect('/carts/%s' % uid)
    else:
        return redirect('/Login/')


def dnc_qty(request, uid, item_id):
    if request.session.get('session_id'):
        try:
            cart_item = cart_items.objects.get(item_id=item_id)
            if cart_item.qty > 1:
                qty = cart_item.qty - 1
            else:
                qty = 1
            cart_item1 = cart_items.objects.filter(item_id=item_id).update(qty=qty)
            return redirect('/carts/%s' % uid)
        except cart_items.DoesNotExist:
            cart_item = None
            return redirect('/carts/%s' % uid)
    else:
        return redirect('/Login/')


def place_order(request, uid, carts_id):
    if request.session.get('session_id'):
        categories = get_category()
        user = User_Reg.objects.get(User_Id=uid)
        cart_item = cart_items.objects.filter(carts_id=carts_id)
        agent = delivery_agent.objects.filter(available=True).first()
        print("-----------------------------------------------------------", agent)
        total_price = 0
        order_date = datetime.now().date()
        for i in cart_item:
            total_product_price = i.product_id.Price * i.qty
            pickup_date = datetime.now() + timedelta(days=1)
            cart_item1 = cart_items.objects.get(item_id=i.item_id)
            total_price = total_price + total_product_price
            orders.objects.create(cart_item_id=cart_item1, pickup_date=pickup_date,
                                  total_product_price=total_product_price, user_id=user, order_date=order_date,
                                  agents_id=agent)
        return render(request, "orders/place_order.html",
                      {'cart_item': cart_item, 'login_id': uid, 'categories': categories, 'total_price': total_price,
                       'cart_id': carts_id})
    else:
        return redirect('/Login/')


def checkout(request, uid, total_price, cart_id):
    if request.session.get('session_id'):
        categories = get_category()
        agent = orders.objects.filter(cart_item_id__carts_id=cart_id).values('agents_id').distinct().first()
        cart.objects.filter(user_id=uid).update(status=False)
        agent_id = agent['agents_id']
        delivery_agent.objects.filter(agent_id=agent_id).update(available=False)
        agent1 = delivery_agent.objects.get(agent_id=agent_id)
        return render(request, "orders/checkout.html",
                      {'agent': agent1, 'login_id': uid, 'categories': categories, 'total_price': total_price})
    else:
        return redirect('/Login/')


def order_history(request, uid):
    if request.session.get('session_id'):
        order = orders.objects.filter(user_id=uid)
        categories = get_category()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "User/orders.html", {'page_obj': page_obj, 'login_id': uid, 'categories': categories})
    else:
        return redirect('/Login/')


def new_order(request, uid):
    if request.session.get('session_id'):
        order = orders.objects.filter(cart_item_id__farmers_id=uid).order_by('order_date')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Farmer/new_orders.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/Login/')


def delivery_agent_orders(request, uid):
    if request.session.get('session_id'):
        order_list = orders.objects.filter(Q(agents_id=uid) & Q(deliver_status=False)).order_by('order_date')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "delivery/my_orders.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/Login/')


def pickup_order(request, uid, id):
    if request.session.get('session_id'):
        orders.objects.filter(order_id=id).update(pickup_status=True)
        return redirect('/delivery_agent_orders/%s' % uid)
    else:
        return redirect('/Login/')


def deliver_order(request, uid, id):
    if request.session.get('session_id'):
        orders.objects.filter(order_id=id).update(deliver_status=True)
        delivery_agent.objects.filter(agent_id=uid).update(available=True)
        return redirect('/delivery_agent_orders/%s' % uid)
    else:
        return redirect('/Login/')


def product_more_details(request, uid, id):
    if request.session.get('session_id'):
        products = Product.objects.get(Product_Id=id)
        categories = get_category()
        return render(request, "User/product_more_details.html",
                      {'products': products, 'login_id': uid, 'categories': categories})
    else:
        return redirect('/Login/')


def edit_agent(request, uid, id):
    if request.session.get('session_id'):
        agent = delivery_agent.objects.get(agent_id=id)
        if request.method == 'POST':
            form = edit_agentform(request.POST, instance=agent)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/delivery_agent_list/%s' % uid)
        else:
            form_value = edit_agentform(instance=agent)
            return render(request, "Admin/delivery_agent_list.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def add_govt_policy(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = add_policyform(request.POST, request.FILES)
            if form.is_valid():
                caption = form.cleaned_data['caption']
                img = form.files['image']
                lastdate = form.cleaned_data['lastdate']
                user_id = User_Reg.objects.get(User_Id=uid)
                govt_policies.objects.create(caption=caption, image=img, user_id=user_id, lastdate=lastdate)
                messages.warning(request, "Policy Added Successfully")
                return redirect('/add_govt_policy/%s' % uid)
        else:
            form_value = add_policyform()
            return render(request, "govt/add_govt_policy.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def admin_policy_list(request, uid):
    if request.session.get('session_id'):
        policy = govt_policies.objects.all().order_by('-uploaded_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(policy, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Admin/policy_list.html",
                      {'policy': policy, 'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/Login/')


def farmer_policy_list(request, uid):
    if request.session.get('session_id'):
        policy = govt_policies.objects.all().order_by('-uploaded_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(policy, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Farmer/policy_list.html",
                      {'policy': policy, 'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/Login/')


def delete_policy(request, uid, id):
    if request.session.get('session_id'):
        govt_policies.objects.filter(policy_id=id).delete()
        return redirect('/admin_policy_list/%s' % uid)
    else:
        return redirect('/Login/')


def edit_policy(request, uid, id):
    if request.session.get('session_id'):
        policy = govt_policies.objects.get(policy_id=id)
        if request.method == 'POST':
            form = edit_policyform(request.POST, instance=policy)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/admin_policy_list/%s' % uid)
        else:
            form_value = edit_policyform(instance=policy)
            return render(request, "govt/edit_policy.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def add_tip_category(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = add_catform(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, "Category Added Successfully")
                return redirect('/add_tip_category/%s' % uid)
        else:
            form_value = add_catform()
            return render(request, "Admin/add_tip_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def edit_tip_category(request, uid, id):
    if request.session.get('session_id'):
        categories = tip_category.objects.get(tip_cat_id=id)
        if request.method == 'POST':
            form = edit_categoryForm(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/list_tip_category/%s' % uid)
        else:
            form_value = edit_categoryForm(instance=categories)
            return render(request, "Admin/edit_tip_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def list_tip_category(request, uid):
    if request.session.get('session_id'):
        categories = tip_category.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Admin/list_tip_category.html",
                      {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def delete_tip_category(request, uid, id):
    if request.session.get('session_id'):
        tip_category.objects.get(tip_cat_id=id).delete()
        return redirect('/list_tip_category/%s' % uid)
    else:
        return redirect('/Login/')


def add_tips(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = add_tipsform(request.POST, request.FILES)
            if form.is_valid():
                description = form.cleaned_data['description']
                img = form.files['image']

                categories = form.cleaned_data['category']
                farmhouse_id = FarmHouse_Reg.objects.get(FarmHouse_Id=uid)
                tips.objects.create(category=categories, description=description, image=img, farmhouse=farmhouse_id)
                messages.warning(request, "Tips Added Successfully")
                return redirect('/add_tips/%s' % uid)
        else:
            form_value = add_tipsform()
            return render(request, "FarmHouse/add_tips.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def edit_tips(request, uid, id):
    if request.session.get('session_id'):
        categories = tips.objects.get(tip_id=id)
        if request.method == 'POST':
            form = edit_tipsform(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/list_tips/%s' % uid)
        else:
            form_value = edit_tipsform(instance=categories)
            return render(request, "FarmHouse/edit_tips.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def list_tips(request, uid):
    if request.session.get('session_id'):
        categories = tips.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "FarmHouse/list_tips.html",
                      {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def delete_tips(request, uid, id):
    if request.session.get('session_id'):
        tips.objects.get(tip_id=id).delete()
        return redirect('/list_tips/%s' % uid)
    else:
        return redirect('/Login/')


def userpost(request, uid):
    if request.session.get('session_id'):
        tip = tips.objects.all()
        return render(request, 'User/post.html', {'tip': tip, 'login_id': uid})
    else:
        return redirect('/Login/')


def farmerpost(request, uid):
    if request.session.get('session_id'):
        tip = tips.objects.all()
        return render(request, 'Farmer/post.html', {'tip': tip, 'login_id': uid})
    else:
        return redirect('/Login/')


def add_machinery(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = add_machineryform(request.POST, request.FILES)
            if form.is_valid():
                categories = form.cleaned_data['categories']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']
                image = form.files['image']
                farmhouse_id = FarmHouse_Reg.objects.get(FarmHouse_Id=uid)
                rental_product.objects.create(categories=categories, name=name, description=description, price=price,
                                              image=image,
                                              farmhouse_id=farmhouse_id)
                messages.warning(request, "Machines Added Successfully")
                return redirect('/add_machinery/%s' % uid)
        else:
            form_value = add_machineryform()
            return render(request, "machinery/add_machinery.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def edit_machinery(request, uid, id):
    if request.session.get('session_id'):
        machinery = rental_product.objects.get(machine_id=id)
        if request.method == 'POST':
            form = edit_machineryform(request.POST, request.FILES, instance=machinery)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/machinery_list/%s' % uid)
        else:
            form_value = edit_machineryform(instance=machinery)
            return render(request, "machinery/edit_machinery.html",
                          {'form_key': form_value, 'machinery': machinery, 'login_id': uid})
    else:
        return redirect('/Login/')


def machinery_list(request, uid):
    if request.session.get('session_id'):
        machinery = rental_product.objects.filter(farmhouse_id=uid)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(machinery, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "machinery/machinery_list.html",
                      {'machinery': machinery, 'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/Login/')


def delete_machinery(request, uid, id):
    if request.session.get('session_id'):
        rental_product.objects.get(machine_id=id).delete()
        return redirect('/machinery_list/%s' % uid)
    else:
        return redirect('/Login/')


def add_machine_category(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = add_machine_categoryform(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, "Category Added Successfully")
                return redirect('/add_machine_category/%s' % uid)
        else:
            form_value = add_machine_categoryform()
            return render(request, "Admin/add_machine_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def edit_machine_category(request, uid, id):
    if request.session.get('session_id'):
        categories = rental_category.objects.get(category_id=id)
        if request.method == 'POST':
            form = edit_machine_categoryform(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/list_machine_category/%s' % uid)
        else:
            form_value = edit_machine_categoryform(instance=categories)
            return render(request, "Admin/edit_machine_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/Login/')


def list_machine_category(request, uid):
    if request.session.get('session_id'):
        categories = rental_category.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Admin/list_machine_category.html",
                      {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/Login/')


def delete_machine_category(request, uid, id):
    if request.session.get('session_id'):
        rental_category.objects.get(category_id=id).delete()
        return redirect('/list_machine_category/%s' % uid)
    else:
        return redirect('/Login/')


def get_machinery(request, uid, id):
    if request.session.get('session_id'):
        machinery = rental_product.objects.filter(categories=id)
        category = get_rentalcategory()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(machinery, 8)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "Farmer/view_machinery.html",
                      {'page_obj': page_obj, 'login_id': uid, 'category': category})
    else:
        return redirect('/Login/')


def machinery_more_details(request, uid, id):
    if request.session.get('session_id'):
        products = rental_product.objects.get(machine_id=id)
        category = get_rentalcategory()
        return render(request, "Farmer/machinery_more_details.html",
                      {'products': products, 'login_id': uid, 'category': category})
    else:
        return redirect('/Login/')


def farmer_machine_request(request, uid, fid, mid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = Request_form(request.POST)
            if form.is_valid():
                no_of_days = form.cleaned_data['no_of_days']
                farmhouse_id = FarmHouse_Reg.objects.get(FarmHouse_Id=fid)
                farmer_id = Farmer_Reg.objects.get(Farmer_Id=uid)
                machine_id = rental_product.objects.get(machine_id=mid)
                rental_request.objects.create(no_of_days=no_of_days, farmhouse_id=farmhouse_id, farmer_id=farmer_id,
                                              machine_id=machine_id)
                messages.warning(request, "Rental Request Send Successfully")
                return redirect('/machinery_more_details/%s/%s' % (uid, mid))
        else:
            form = Request_form()
            return render(request, "Farmer/request_form.html", {'form_key': form, 'login_id': uid})
    else:
        return redirect('/Login/')


def view_rental_request(request, uid):
    if request.session.get('session_id'):
        req = rental_request.objects.filter(Q(farmhouse_id=uid) & Q(req_status=True) & Q(rental_status=False))
        if req:
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'FarmHouse/rental_request.html', {'page_obj': page_obj, 'login_id': uid, 'count': 1})
        else:
            messages.warning(request, "No New Requests")
            return render(request, "FarmHouse/rental_request.html", {'login_id': uid, 'count': 0})

    else:
        return redirect('/Login/')


def approve_request(request, uid, id):
    if request.session.get('session_id'):
        rental = rental_request.objects.filter(req_id=id).update(rental_status=True)
        req = rental_request.objects.get(req_id=id)
        fname = req.farmer_id.First_Name
        lname = req.farmer_id.Last_Name
        frmhouse = req.farmhouse_id.First_Name
        machine = req.machine_id.name
        subject = 'Rental Request Approved'
        message = f'Hi {fname} {lname},I am {frmhouse} Your Rental Request For {machine} has been approved. Our agent will deliver the product by tomorrow evening and Pick-up will take place on the evening of the last day you specified.\n' \
                  f'Note : The entire cost of the machine will be charged for any damage done to it. . \n' \
                  f'Thank you..'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['fathimamp37@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)
        messages.warning(request, "Rental Request Approved")
        return redirect('/view_rental_request/%s' % uid)
    else:
        return render('/Login/')


def reject_request(request, uid, id):
    if request.session.get('session_id'):
        service = rental_request.objects.filter(req_id=id).delete()
        return redirect('/view_rental_request/%s' % uid)
    else:
        return redirect('/Login/')


def rented_machines(request, uid):
    if request.session.get('session_id'):
        req = rental_request.objects.filter(Q(farmhouse_id=uid) & Q(req_status=True) & Q(rental_status=True))
        if req:
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'FarmHouse/rented_products.html',
                          {'page_obj': page_obj, 'login_id': uid, 'count': 1})
        else:
            messages.warning(request, "There are currently no rented products.")
            return render(request, "FarmHouse/rented_products.html", {'login_id': uid, 'count': 0})

    else:
        return redirect('/Login/')


def machine_collected(request, uid, id):
    if request.session.get('session_id'):
        service = rental_request.objects.filter(req_id=id).update(req_status=False, rental_status=False)
        return redirect('/rented_machines/%s' % uid)
    else:
        return render('/Login/')


def previous_rented_machines(request, uid):
    if request.session.get('session_id'):
        req = rental_request.objects.filter(Q(farmhouse_id=uid) & Q(req_status=False) & Q(rental_status=False))
        if req:
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'FarmHouse/previous_rented_machines.html',
                          {'page_obj': page_obj, 'login_id': uid, 'count': 1})
        else:
            messages.warning(request, "There are currently no previous rented machines.")
            return render(request, "FarmHouse/previous_rented_machines.html", {'login_id': uid, 'count': 0})

    else:
        return redirect('/Login/')


def view_farmer_rental_request(request, uid):
    if request.session.get('session_id'):
        req = rental_request.objects.filter(Q(farmer_id=uid) & Q(req_status=True) & Q(rental_status=False))
        if req:
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'Farmer/rental_request.html', {'page_obj': page_obj, 'login_id': uid, 'count': 1})
        else:
            messages.warning(request, "No New Requests")
            return render(request, "Farmer/rental_request.html", {'login_id': uid, 'count': 0})

    else:
        return redirect('/Login/')


def farmer_rented_machines(request, uid):
    if request.session.get('session_id'):
        req = rental_request.objects.filter(Q(farmer_id=uid) & Q(req_status=True) & Q(rental_status=True))
        if req:
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'Farmer/rented_products.html', {'page_obj': page_obj, 'login_id': uid, 'count': 1})
        else:
            messages.warning(request, "There are currently no rented products.")
            return render(request, "Farmer/rented_products.html", {'login_id': uid, 'count': 0})

    else:
        return redirect('/Login/')


def farmer_previous_rented_machines(request, uid):
    if request.session.get('session_id'):
        req = rental_request.objects.filter(Q(farmer_id=uid) & Q(req_status=False) & Q(rental_status=False))
        if req:
            page_num = request.GET.get('page', 1)
            paginator = Paginator(req, 5)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return render(request, 'Farmer/previous_rented_machines.html',
                          {'page_obj': page_obj, 'login_id': uid, 'count': 1})
        else:
            messages.warning(request, "There are currently no previous rented machines.")
            return render(request, "Farmer/previous_rented_machines.html", {'login_id': uid, 'count': 0})

    else:
        return redirect('/Login/')


def get_rentalcategory():
    category = rental_category.objects.all()
    return category
