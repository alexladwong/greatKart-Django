from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("dashboard/", views.Dashboard, name="my-dashboard"),
    path("", views.Dashboard, name="my-dashboard"),
    # Account verification url.
    path("activate/<uidb64>/<token>/", views.Activate, name="activate"),
    path(
        "resetpassword_validator/<uidb64>/<token>/",
        views.ResetPassword_Validator,
        name="resetpassword_validator",
    ),
    path("forgotPassword/", views.ForgotPassword, name="forgotpassword"),
    path("PasswordReset/", views.PasswordReset, name="resetpassword"),
    path("my-orders/", views.MyOrders, name="my_orders"),
]
