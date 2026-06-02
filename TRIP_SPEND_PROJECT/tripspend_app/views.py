from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from .models import Trip, Expense, ExpenseCategory


# ---------------- AUTH ---------------- #

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect("trip_list")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("trip_list")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- TRIPS ---------------- #

@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    today = date.today()

    active_trips = trips.filter(
        start_date__lte=today,
        end_date__gte=today
    ).count()

    total_expense = Expense.objects.filter(
        trip__user=request.user
    ).aggregate(total=Sum('amount'))['total'] or 0

    return render(request, "trip_list.html", {
        "trips": trips,
        "active_trips": active_trips,
        "total_expense": total_expense,
        "today": today,
    })


@login_required
def trip_create(request):
    if request.method == "POST":
        Trip.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            destination=request.POST.get("destination"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date")
        )
        return redirect("trip_list")

    return render(request, "trip_create.html")


@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    expenses = trip.expenses.all()
    total = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    return render(request, "trip_detail.html", {
        "trip": trip,
        "expenses": expenses,
        "total": total
    })


@login_required
def add_expense(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    categories = ExpenseCategory.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        category = ExpenseCategory.objects.get(id=category_id) if category_id else None

        Expense.objects.create(
            trip=trip,
            category=category,
            description=request.POST.get("description"),
            amount=request.POST.get("amount"),
            date=request.POST.get("date")
        )
        return redirect("trip_detail", pk=trip.pk)

    return render(request, "expense_form.html", {
        "trip": trip,
        "categories": categories
    })


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    trip_id = expense.trip.pk
    expense.delete()
    return redirect("trip_detail", pk=trip_id)

def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    categories = ExpenseCategory.objects.all()

    if request.method == "POST":
        expense.description = request.POST.get("description")
        expense.amount = request.POST.get("amount")

        date_value = request.POST.get("date")
        if date_value:
            expense.date = date_value

        category_id = request.POST.get("category")
        if category_id:
            expense.category = ExpenseCategory.objects.get(id=category_id)
        else:
            expense.category = None

        expense.save()
        return redirect("trip_detail", pk=expense.trip.pk)

    return render(request, "expense_form.html", {
        "expense": expense,
        "categories": categories,
    })
@login_required
def profile(request):
    total_trips = Trip.objects.filter(
        user=request.user
    ).count()

    total_expenses = Expense.objects.filter(
        trip__user=request.user
    ).aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    return render(
        request,
        "profile.html",
        {
            "total_trips": total_trips,
            "total_expenses": total_expenses,
        }
    )