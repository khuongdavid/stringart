from django.shortcuts import render, redirect
from django.views import View
from art.models import Art
from django.contrib import messages
import os
from .algorithm.generate import create_string_art
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from django.conf import settings
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Art, Categories
from user.models import User
from django.core.files import File
import uuid

# Create your views here.
class ArtDetailView(View):
    def get(self, request, art_id):
        art = Art.objects.get(id=art_id)
        return render(request, 'art/art_deltail.html', {'art': art})
    def post(self, request, art_id):
        art = Art.objects.get(id=art_id)
        return render(request, 'art/art_deltail.html', {'art': art})


class CreateArtView(View):
    def get(self, request):
        # Lấy đường dẫn ảnh kết quả từ session
        image_result = request.session.get('image_path', None)
        image_root = request.session.get('image_root', None)
        wb = request.session.get('wb_{}'.format(image_result), None)
        rgb = request.session.get('rgb_{}'.format(image_result), None)
        rect = request.session.get('rect_{}'.format(image_result), None)
        if request.session.get('image_processed_{}'.format(image_result), False):
            return render(request, 'art/create_art.html', {'image_processed'.format(image_result): True,
                                                            'image_result': image_result,
                                                            'image_root': image_root,
                                                            'wb': wb,
                                                            'rgb': rgb,
                                                            'rect': rect})
        else:
            return render(request, 'art/create_art.html', {'image_processed_{}'.format(image_result): False,
                                                            'image_result': image_result,
                                                            'image_root': image_root,
                                                            'wb': wb,
                                                            'rgb': rgb,
                                                            'rect': rect})
    
    
    def post(self, request):
        if 'image' in request.FILES:
            image = request.FILES['image'] # lấy ảnh từ request
            file_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(file_path, 'wb') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # lấy các giá trị của form
            pull_amount = 2000
            side_len = 300
            export_strength = 0.1
            random_nails = None
            radius1_multiplier = 1
            radius2_multiplier = 1
            nail_step = 4
            wb = False
            rgb = False
            rect = False

            if request.POST.get('pull_amount'):
                pull_amount = int(request.POST.get('pull_amount'))
            if request.POST.get('side_len'):
                side_len = int(request.POST.get('side_len'))
            if request.POST.get('export_strength'):
                export_strength = float(request.POST.get('export_strength'))
            if request.POST.get('random_nails'):
                random_nails = int(request.POST.get('random_nails'))
            if request.POST.get('radius1_multiplier'):
                radius1_multiplier = float(request.POST.get('radius1_multiplier'))
            if request.POST.get('radius2_multiplier'):
                radius2_multiplier = float(request.POST.get('radius2_multiplier'))
            if 'nail_step' in request.POST:
                nail_step = int(request.POST.get('nail_step'))
            if 'wb' in request.POST:
                wb = request.POST['wb'] == 'True'
            if 'rgb' in request.POST:
                rgb = request.POST['rgb'] == 'True'
            if 'rect' in request.POST:
                rect = request.POST['rect'] == 'True'

            # gọi hàm create_string_art
            result = create_string_art(
                                        input_file = file_path,
                                        side_len=side_len,
                                        export_strength=export_strength,
                                        pull_amount=pull_amount,
                                        random_nails=random_nails,
                                        radius1_multiplier=radius1_multiplier,
                                        radius2_multiplier=radius2_multiplier,
                                        nail_step=nail_step,
                                        wb=wb, 
                                        rgb=rgb, 
                                        rect=rect
                                        )
            

            result_path = file_path + '_result.png'  # Đường dẫn của file kết quả
            mpimg.imsave(result_path, result, cmap=plt.get_cmap("gray"), vmin=0.0, vmax=1.0) # tạo và lưu ảnh vào đường dẫn result_path
            image_result = "/Uploads/" + '/'.join(result_path.split('/')[-1:]) # tạo đường dẫn ảnh để gửi về templates
            image_root = "/Uploads/" + '/'.join(file_path.split('/')[-1:]) # tạo đường dẫn đến hình gốc
            # Đặt biến session để xác định việc xử lý đã được thực hiện
            request.session['image_processed_{}'.format(image_result)] = True
            request.session['image_path'] = image_result  # Lưu đường dẫn của file kết quả vào session
            request.session['image_root'] = image_root  # Lưu đường dẫn của file gốc vào session
            request.session['wb_{}'.format(image_result)] = wb
            request.session['rgb_{}'.format(image_result)] = rgb
            request.session['rect_{}'.format(image_result)] = rect
            messages.success(request, 'Hoàn tất tạo tranh chỉ')

            return HttpResponseRedirect(reverse('art:create_art'))

        else:
            messages.error(request, "Lấy file không thành công")
            image_result = None
            return render(request, 'art/create_art.html', {'image_result': image_result})


def save_art(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image_result = os.getcwd() + request.session.get('image_path', None)
        image_root = os.getcwd() + request.session.get('image_root', None)

        wb = request.session.get('wb_{}'.format('image_result'), None)
        rgb = request.session.get('rgb_{}'.format('image_result'), None)
        rect = request.session.get('rect_{}'.format('image_result'), None)
        is_published = request.POST.get('is_published', False)
        if rect == 'True':
            category = Categories.objects.get(name="Rectangular")
        elif rgb == 'True':
            category = Categories.objects.get(name="Circular (colour)")
        else:
            category = Categories.objects.get(name="Circular (black & white)")
        art = Art.objects.create(artists=user, title=title, description=description, categories=category, is_published=is_published)

        unique_identifier = str(uuid.uuid4())[:8] #tạo chuỗi duy nhất gắn với ảnh

        # Thêm phần tử duy nhất vào tên file
        image1_filename = '{}_{}'.format(unique_identifier, image_result.split('/')[-1])
        image2_filename = '{}_{}'.format(unique_identifier, image_root.split('/')[-1])

        # Tạo đối tượng File từ đường dẫn của hình ảnh và gán cho trường image1
        if image_result:
            image1_file = File(open(image_result, 'rb'))
            art.image1.save(image1_filename, image1_file, save=True)

        # Tạo đối tượng File từ đường dẫn của hình ảnh và gán cho trường image2
        if image_root:
            image2_file = File(open(image_root, 'rb'))
            art.image2.save(image2_filename, image2_file, save=True)

        art.save()
        messages.success(request, 'Bạn đã tạo thành công tranh ch')
    
    return HttpResponseRedirect(reverse('art:create_art'))