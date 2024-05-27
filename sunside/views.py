from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def login_user(request):
    logout(request)
    try:
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == "POST":
            username = request.POST['username']
            userpassword = request.POST['password']
            myuser = User.objects.filter(username = username)
            if not myuser.exists():
                messages.warning(request,"Invalid Credentials")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            myuser = authenticate (username = username, password=userpassword)
            if myuser is not None:
                if myuser.is_staff or myuser.is_superuser:
                    login(request, myuser)
                    return redirect(request.POST.get('next', '/'))
                else:
                    messages.warning(request, 'User Unauthorized')
                    return redirect('/login/')
            else:
                messages.warning(request, 'Invalid Password')
                return redirect('/login/')

        return render(request,'login.html')
    except Exception as e:
        print(e)

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')

def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Account Created Successfully')
            return redirect('login_user')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'documentation.html')
    else:
        return render(request, 'index.html')

@login_required
def category(request):
    category = AddCategory()
    context = {'form':category}
    return render(request, 'category/category.html',context)

@login_required
def save_category(request):
    if request.method == "POST":
        form = AddCategory(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if not Category.objects.filter(name=category_name).exists():
                Category.objects.create(name=category_name)
                messages.success(request, 'Category saved successfully.')
            else:
                messages.warning(request, 'Category with the same name already exists.')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form data.')
    else:
        print("Request method is not POST")

    return redirect('/category/')


@login_required
def view_category(request):
    category = Category.objects.order_by('id')
    myfilter = CategoryFilter(request.GET, queryset=category)
    categories = myfilter.qs  # Rename the variable to 'categories' for clarity
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    context = {"categories": categories, 'form': EditCategory(), 'filter': myfilter}
    return render(request, 'category/view_category.html', context)

@login_required
def view_category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {'category': category}
    return render(request, 'category/category_detail.html', context)

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category = get_object_or_404(Category, id=category_id)
        form = EditCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully.')
            return redirect('/viewcategory/')
    else:
        category = Category.objects.get(name= category.name)
        form = EditCategory(instance=category)
    return render(request, 'category/editcategory.html',{'form': form})

@login_required
def delete_category(request, category_id):
    if request.method == "POST":
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Category Deleted Successfully.')
    return redirect('/viewcategory/')

@login_required
def client(request):
    client_form = AddClient()
    context = {'form': client_form}
    return render(request, 'client/client.html', context)

@login_required
def save_client(request):
    if request.method == "POST":
        form = AddClient(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client saved successfully.')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form data.')
    else:
        print("Request method is not POST")

    return redirect('/client/')

@login_required
def view_client(request):
    clients = Client.objects.all()
    paginator = Paginator(clients, 10)
    page = request.GET.get('page')
    clients = paginator.get_page(page)
    context = {'clients': clients}
    return render(request, 'client/view_client.html', context)

@login_required
def view_client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    context = {'client': client}
    return render(request, 'client/client_detail.html', context)

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = EditClient(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('/viewclient/')
    else:
        form = EditClient(instance=client)
    return render(request, 'client/editclient.html', {'form': form})

@login_required
def delete_client(request, client_id):
    if request.method == "POST":
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        messages.success(request, 'Client deleted successfully.')
    return redirect('/viewclient/')