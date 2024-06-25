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
from django.http import JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

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
    search_first_name = request.GET.get('first_name', '')
    search_last_name = request.GET.get('last_name', '')
    search_meter_code = request.GET.get('meter_code', '')

    clients = Client.objects.all()
    
    if search_first_name:
        clients = clients.filter(first_name__icontains=search_first_name)
    if search_last_name:
        clients = clients.filter(last_name__icontains=search_last_name)
    if search_meter_code:
        clients = clients.filter(meter_code__icontains=search_meter_code)
    
    paginator = Paginator(clients, 10)  # Show 10 clients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'client/view_client.html', {'clients': page_obj})

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

@login_required
def get_previous_reading(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
        last_bill = Bill.objects.filter(client=client).order_by('-reading_date').first()
        previous_reading = last_bill.current_reading if last_bill else client.first_reading
        return JsonResponse({'previous_reading': previous_reading})
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    
@login_required
def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.previous_reading = form.cleaned_data['previous_reading']
            bill.total_bill = form.cleaned_data['total_bill']
            bill.save()
            messages.success(request, 'Bill created successfully!')
            return redirect('createbill')  
    else:
        form = BillForm()
        
    return render(request, 'billing/create_bill.html', {'form': form})

@login_required
def list_bills(request):
    bills = Bill.objects.all().select_related('client', 'client__category').order_by('-reading_date')

    client_name = request.GET.get('client_name')
    if client_name:
        bills = bills.filter(client__first_name__icontains=client_name) | bills.filter(client__last_name__icontains=client_name)

    return render(request, 'billing/list_bills.html', {'bills': bills})

@login_required
def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('list_bills') 
    else:
        form = BillForm(instance=bill)
    
    return render(request, 'billing/edit_bill.html', {'form': form, 'bill': bill})

@login_required
def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        bill.delete()
        return redirect('list_bills')
    return render(request, 'billing/delete_bill.html', {'bill': bill})

def print_bill_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    html_string = render_to_string('print_bill_pdf.html', {'bill': bill})
    
    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=bill_{}.pdf'.format(bill.id)
    response['Content-Transfer-Encoding'] = 'binary'
    response.write(result)

    return response
