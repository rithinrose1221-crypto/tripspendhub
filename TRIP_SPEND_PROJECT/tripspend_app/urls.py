from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Trips
    path("", views.trip_list, name="trip_list"),
    path("create/", views.trip_create, name="trip_create"),
    path("<int:pk>/", views.trip_detail, name="trip_detail"),
    path("<int:pk>/add-expense/", views.add_expense, name="add_expense"),
    path("expense/<int:pk>/delete/", views.delete_expense, name="delete_expense"),
    path("expense/<int:pk>/edit/", views.edit_expense, name="edit_expense"),
    path("profile/", views.profile, name="profile"),
]
