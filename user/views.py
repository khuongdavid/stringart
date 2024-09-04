from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm, LoginForm, EditUserForm
from django.contrib.auth import login, logout
from .custom_auth_backend import CustomAuthBackend 
from .models import User, Contact
from django.urls import reverse_lazy
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from PIL import Image
# Create your views here.
class CreateUserView(View, LoginRequiredMixin):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'user/create_user.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')    
                firstname = form.cleaned_data.get('firstname')
                lastname = form.cleaned_data.get('lastname')
                email = form.cleaned_data.get('email')
                user = User.objects.create_user(username=username, 
                                                email=email, 
                                                password=password, 
                                                firstname=firstname, 
                                                lastname=lastname)
                if user:
                    user.save()
                    login(request, user)  # Xác thực người dùng ngay sau khi đăng ký
                    messages.success(request, "Đăng ký thành công")
                    return render(request, 'home/home.html')  # Điều hướng về trang home
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{error}")
                    return render(request, 'user/create_user.html', {'form': form})
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
                return render(request, 'user/create_user.html', {'form': form})
        except User.DoesNotExist:
            messages.error(request, "Tạo user thất bại")
            return render(request, 'user/create_user.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = CustomAuthBackend().authenticate(request=request, username=username, password=password)

            if user is not None:
                if login(request, user) != False:
                    messages.success(request, "Đăng nhập thành công")
                    return redirect(reverse('home:home'))
                else:
                    messages.error(request, 'Login failed')
                    return render(request, 'user/login.html')
            else: 
                messages.error(request, "Tên người dùng hoặc mật khẩu không đúng")
                return render(request, 'user/login.html', {'form': form})
        else:
            error_message = form.errors.as_text()
            messages.error(request, f"{error_message}")
        
        return render(request, 'user/login.html', {'form': form})


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect(reverse('home:home'))


class EditUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = EditUserForm(instance=user)
        return render(request, 'user/edit_user.html', {'form': form})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = EditUserForm(request.POST, request.FILES, instance=user)
        try:
            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                oldpassword = form.cleaned_data.get('oldpassword')
                newpassword = form.cleaned_data.get('newpassword')
                username = user.username

                if CustomAuthBackend().authenticate(request=request, username=username, password=oldpassword) is not None: #kiem tra mat khau
                    if firstname != '':
                        user.firstname = firstname
                    if lastname != '':
                        user.lastname = lastname
                    if email != '':
                        user.email = email
                    if newpassword!= '':
                        user.set_password(newpassword)
                    if 'image' in request.FILES:
                        # Lấy file từ request
                        uploaded_file = request.FILES['image']

                        # Kiểm tra kiểu file sử dụng Pillow
                        try:
                            img = Image.open(uploaded_file)
                            img.verify()  # Thực hiện kiểm tra file
                        except:
                            messages.error(request, "File truyền vào không phải là hình ảnh hoặc PDF!")
                            return HttpResponseRedirect(reverse('user:edit_user', args=[user.id]))

                        # Kiểm tra và xác nhận kiểu MIME của file
                        if not uploaded_file.content_type.startswith('image/') and not uploaded_file.content_type == 'application/pdf':
                            messages.error(request, "File truyền vào không phải là hình ảnh hoặc PDF!")
                            return HttpResponseRedirect(reverse('user:edit_user', args=[user.id]))

                        if user.image:
                            os.remove(user.image.path)  # Xóa tệp hình ảnh cũ
                        user.image = uploaded_file  # Lưu tệp hình ảnh mới vào đối tượng User
                    user.save()

                    login(request, user)  # Xác thực người dùng ngay sau khi sửa đổi
                    messages.success(request, "Cập nhật thành công")
                    return HttpResponseRedirect(reverse('user:edit_user', args=[user.id]))
                else:
                        error_message = form.errors.as_text()
                        messages.error(request, f"Sai mật khẩu! {error_message}")
                        return HttpResponseRedirect(reverse('user:edit_user', args=[user.id]))
            else:
                error_message = form.errors.as_text()
                messages.error(request, f"Cập nhật thất bại! {error_message}")
                return HttpResponseRedirect(reverse('user:edit_user', args=[user.id]))  

        except User.DoesNotExist:
            messages.error(request, "Cập nhật thất bại")
            return HttpResponseRedirect(reverse('user:edit_user', args=[user.id]))  # Redirect to home page


def contact_submit(request, user_id=None):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            user = None
        else:
            user = User.objects.get(id=user_id)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact(firstname=firstname, lastname=lastname, email=email, message=message, user=user)
        contact.save()
        messages.success(request, "Gửi liên hệ thành công")
        return redirect(reverse('home:home'))