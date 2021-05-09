from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Expense
from .forms import ExpenseForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from .filters import ExpenseFilter


@unauthenticated_user
def register_page(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(
                request, f"Account was successfully created for {username}")

            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'expense/register.html', context)


@unauthenticated_user
def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password in incorrect")
    context = {}

    return render(request, 'expense/login.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def home(request):

    user = request.user
    print(user)

    expenses = Expense.objects.filter(user=user)

    my_filter = ExpenseFilter(request.GET, queryset=expenses)
    expenses = my_filter.qs

    total = 0
    for expense in expenses:
        total = total + int(expense.amount)
    print(total)

    context = {
        'my_filter': my_filter,
        'expenses': expenses,
        'total': total,
    }

    return render(request, 'expense/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def add_expense(request):

    form = ExpenseForm()

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'expense/expense_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def update_expense(request, pk):

    expense = Expense.objects.get(id=pk)

    form = ExpenseForm(instance=expense)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'expense/expense_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def delete_expense(request, pk):

    expense = Expense.objects.get(id=pk)

    if request.method == "POST":
        expense.delete()
        return redirect('/')

    context = {
        "expense": expense
    }

    return render(request, 'expense/delete_confirm.html', context)
