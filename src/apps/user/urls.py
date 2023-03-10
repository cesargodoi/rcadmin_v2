from django.urls import path
from django.contrib.auth import views
from . import views as user_views


# user
urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(template_name="user/auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(template_name="user/auth/logout.html"),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="user/auth/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="user/auth/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="user/auth/password_reset_form.html",
            email_template_name="user/auth/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done",
        views.PasswordResetDoneView.as_view(
            template_name="user/auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="user/auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done",
        views.PasswordResetCompleteView.as_view(
            template_name="user/auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

# profile
urlpatterns += [
    path("profile/detail/", user_views.profile_detail, name="profile_detail"),
    path(
        "profile/updt_profile/", user_views.updt_profile, name="updt_profile"
    ),
    path("profile/updt_image/", user_views.updt_image, name="updt_image"),
    path(
        "profile/historic/",
        user_views.user_historic,
        name="user_historic",
    ),
    path(
        "profile/frequencies/",
        user_views.user_frequencies,
        name="user_frequencies",
    ),
    path(
        "profile/frequencies/scan_qrcode_event/",
        user_views.scan_qrcode_event,
        name="scan_qrcode_event",
    ),
    path(
        "profile/payments/",
        user_views.user_payments,
        name="user_payments",
    ),
    path(
        "profile/new-order/",
        user_views.user_new_order,
        name="user_new_order",
    ),
    path(
        "profile/add-payment/",
        user_views.user_add_payment,
        name="user_add_payment",
    ),
    path(
        "profile/how-to-pay/",
        user_views.user_how_to_pay,
        name="user_how_to_pay",
    ),
    path(
        "profile/del-payment/<int:pay_id>/",
        user_views.user_del_payment,
        name="user_del_payment",
    ),
]
