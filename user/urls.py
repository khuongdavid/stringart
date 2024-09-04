from django.urls import path
from .views import CreateUserView, LoginView, LogoutView, EditUserView, contact_submit
app_name = 'user'

urlpatterns = [
    path("create_user/", CreateUserView.as_view(), name = "create_user"),
    path("login/", LoginView.as_view(), name = "login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path("edit/<int:user_id>/", EditUserView.as_view(), name = "edit_user"),
    path("contact/<int:user_id>/", contact_submit, name = "contact"),
    path("contact/", contact_submit, name = "contact_no_id"),
]

