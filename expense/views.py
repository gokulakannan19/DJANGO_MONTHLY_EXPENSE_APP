from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .models import Expense
from .forms import ExpenseForm, CreateUserForm


def register_page(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(
                request, f"Account was successfully created for {user}")

            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'expense/register.html', context)


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


def logout_user(request):
    logout(request)
    return redirect('login')


def home(request):

    expenses = Expense.objects.all()

    context = {
        'expenses': expenses,
    }

    return render(request, 'expense/home.html', context)


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


def delete_expense(request, pk):

    expense = Expense.objects.get(id=pk)

    if request.method == "POST":
        expense.delete()
        return redirect('/')

    context = {
        "expense": expense
    }

    return render(request, 'expense/delete_confirm.html', context)
