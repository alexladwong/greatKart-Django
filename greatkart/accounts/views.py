from django.shortcuts import get_object_or_404, redirect, render

from carts.models import *
from orders.models import Order, orderProducts
from .forms import *
from .models import *
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id

# Send Email Verifications
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests


# Create your views here.
def Register(request):  # Registration form functionality
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            # Create User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = "default/default-user.png"
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please Activate your account"
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            # # Explicitly set microsecond to 0
            # token = token.replace(microsecond=0)
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(
            #     request,
            #     "Thank you for registering with us. Please Check your E-mail. We just sent you the Activation Link. ",
            # )
            return redirect("/accounts/login/?command=verification&email=" + email)

    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


# END Registration


# LOGIN ACC
def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Group the product variation by id:
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # Get the Cart item from the User to access the variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(
                request,
                f"Welcome Back { user.first_name }! You are logged in Successfully!",
            )

            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query

                # next=/cart/checkout/
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                return redirect("my-dashboard")
        else:
            messages.error(request, "Invalid Login Credentials, please try again")
            return redirect("login")
    return render(request, "accounts/login.html")


# END LOGIN ACC


# LOGOUT ACC
@login_required(login_url="login")
def Logout(request):
    auth.logout(request)
    messages.success(request, f"Bye Bye! You Just logged Out!")
    return redirect("login")


# Account Activations
def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (ValueError, TypeError, OverflowError, Account.DoesNotExists):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account is Activated successfully!")

        return redirect("login")
    else:
        messages.error(request, "Invalid Activation Link!")
        return redirect("register")


# Dashboard
@login_required(login_url="login")
def Dashboard(request):
    orders = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id, is_ordered=True
    )
    orders_count = orders.count()
    context = {
        "orders_count": orders_count,
    }
    return render(request, "accounts/dashboard.html", context)


# ForgotPassword(password reset password)
def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # RESET PASSWORD EMAIL
            current_site = get_current_site(request)
            mail_subject = "Please Reset Your Password!"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            # # Explicitly set microsecond to 0
            # token = token.replace(microsecond=0)
            to_email = email
            rest_password = EmailMessage(mail_subject, message, to=[to_email])
            rest_password.send()

            messages.success(
                request, "Password Reset Email has been sent to your Email Address!"
            )
            return redirect("login")

        else:
            messages.error(request, "Account does not exist")
            return redirect("forgotpassword")
    return render(request, "accounts/reset_password.html")


# ResetPassword_Validator
@login_required(login_url="login")
def ResetPassword_Validator(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (ValueError, TypeError, OverflowError, Account.DoesNotExists):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        # user.save()
        messages.info(request, "Please Reset Your Password!")

        return redirect("resetpassword")
    else:
        messages.error(request, "This link has Expired!")
        return redirect("forgotpassword")


# PasswordReset
@login_required(login_url="login")
def PasswordReset(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Your password has been reset successfully!")
            return redirect("login")

        else:
            messages.error(request, "Password Reset Failed, Password Don't Match!")
            return redirect("resetpassword")
    else:
        return render(request, "accounts/password_resetAll.html")


# MyOrders
@login_required(login_url="login")
def MyOrders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    context = {
        "orders": orders,
    }
    return render(request, "accounts/myOrders.html", context)


# EditProfile
@login_required(login_url="login")
def EditProfile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # userprofile.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect("edit_profile")
        else:
            messages.error(
                request,
                "An error occurred. Please check the form.",
            )

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "userprofile": userprofile,
    }

    return render(request, "accounts/edit_profile.html", context)


# ChangeProfilePassword
@login_required(login_url="login")
def ChangeProfilePassword(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        # User objects
        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, "Password changed successfully!")
                return redirect("change_profile_password")
            else:
                messages.error(
                    request, "Please Check your current password and try again."
                )
                return redirect("change_profile_password")
        else:
            messages.error(request, "Password does not match!")
            return redirect("change_profile_password")
    return render(request, "accounts/change_profile_password.html")


# OrderDetails
@login_required(login_url="login")
def OrderDetails(request, timestamp):
    order_details = orderProducts.objects.filter(order__order_number=timestamp)
    order = Order.objects.get(order_number=timestamp)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
    context = {
        "order_details": order_details,
        "order": order,
        "subtotal": subtotal,
    }
    return render(request, "accounts/order_details.html", context)
