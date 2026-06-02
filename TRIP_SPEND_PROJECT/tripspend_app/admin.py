from django.contrib import admin
from tripspend_app.models import Trip, ExpenseCategory, Expense

admin.site.register(Trip)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)
