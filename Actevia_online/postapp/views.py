import re
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import Post ,CommentPost ,Like ,ReplyPost,Notification
from postapp.forms import PostForm , CommentForm
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from qrcode import *
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.contrib.auth.models import User
from onlinexam.views import admin_login
from teacher.views import teacher_signIn




def download_video(request, pk):
    video = get_object_or_404(Post, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()






def see_video(request):
    video_list = Post.objects.filter(teacher=request.user.teacher)
    
    return render(request ,"post/imag.html" ,{"video":video_list})

def search(request):
    query = request.GET.get('q')
    if query:
        videos = Post.objects.filter(title__icontains=query)
    else:
        videos = Post.objects.all()
    return render(request, 'post/imag.html', {'video': videos})


def like(request,pk):
    video = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=request.POST.get('like_id'))
    if request.user.is_authenticated:
        if post.liked.filter(id=request.user.id).exists():
            post.liked.remove(request.user)
        else:
            post.liked.add(request.user)
    else:
        # Handle the case where the user is not authenticated
        # For example, you could redirect them to the login page
        return HttpResponse("login problem")
        


    return HttpResponseRedirect(reverse('detail_video', args=[str(pk)]))



def admin_see_video(request, pk):
    video = get_object_or_404(Post, pk=pk)
    
    context = {
            'video': video,
            }
    return render(request, 'post/admin_see_video.html' ,context)
    



def detail_video(request,pk):

    video1= Post.objects.get(id=pk)
    
    video = Post.objects.all()
    video_post = Post.objects.get(pk=pk)
    comments = CommentPost.objects.filter(video=video_post)
    comment_form = CommentForm()
    if request.method == 'POST':
          comment_form = CommentForm(request.POST)
          if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.video = video1
            comment.user = request.user
            comment.save()

            pattern = r'@(?P<username>\w+)'
            mention_usernames = re.findall(pattern, comment.content)
            for username in mention_usernames:
                try:
                    mentioned_user = User.objects.get(username=username)
                    notification = Notification.objects.create(
                        recipient=mentioned_user,
                        actor=request.user,
                        verb='mentioned you in a comment',
                        target=video1,
                    )
                except User.DoesNotExist:
                    # handle case where user does not exist
                    pass
            return redirect("video_detail" ,pk=pk)
          
    else:
        comment_form = CommentForm()
    
    return render(request, 'post/video_detail.html', {'video': video1  ,"form":CommentForm ,"comment":comments})

def suggest_usernames(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query)
    usernames = [user.username for user in users]
    return JsonResponse(usernames, safe=False)



def video_comments(request,pk):
    video = Post.objects.all()
    video_post = Post.objects.get(pk=pk)

    comments = CommentPost.objects.filter(video=video_post)
    context = {'video_post': video_post, 'comments': comments}
    return render(request, 'post/comment.html', context)




def delete_comment(request, pk):
    
    comment = CommentPost.objects.get(pk=pk)
    comment.delete()
    return redirect('video_detail', pk=comment.video.pk)

def reply_comment(request, pk):
    comment = CommentPost.objects.get(pk=pk)

    if request.method == 'POST':
        author = request.user
        text = request.POST.get('text')
        reply = ReplyPost(comment=comment, author=author, text=text)
        reply.save()

    return redirect('video_detail', pk=comment.video.pk)


def view_video(request):
    teacher = request.user.teacher_profile
    video = Post.objects.filter(teacher=teacher)
    
    return render(request, 'post/view_video.html', {"video": video})

def qr_code(request, pk):
    my_model = get_object_or_404(Post, pk=pk)
    data = f"{my_model.description} \n {my_model.title} \n {my_model.created}"
    img = qrcode.make(data, box_size=10, border=4)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response
    



data = None
def home(request):
    global data
    if request.method=="POST":
        data=request.POST['data']
        img=make(data)
        img.save("static/image/test.png")
        return HttpResponseRedirect("/home")
    else:
        pass
    return render(request,"post/home.html",{'data':data})




def post_detail1(request, pk):
    return HttpResponse("this is qrcode")


from django.core.exceptions import ValidationError

def create_video_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            if 'posti' in request.FILES:
                image_file = request.FILES['posti']
                try:
                    # Validate the image file
                    form.fields['posti'].clean(image_file)
                    post.posti = image_file
                except ValidationError:
                    # Handle validation error
                    form.add_error('posti', 'Upload a valid image file.')

            if 'video_file' in request.FILES:
                video_file = request.FILES['video_file']
                post.video_file = video_file
                post.teacher = request.user.teacher_profile

            post.save()
            return redirect("/teacher/teacher_video")
    else:
        form = PostForm()
    return render(request, 'post/create_video_form.html', {'form': form})


@login_required(login_url='/teacher/teacher_signIn')
def update_video_form(request ,pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/video/view_video')
    return render(request, 'post/update_video_form.html', {'form': form})


@login_required(login_url='/teacher/teacher_signIn')
def delete_video_form(request,pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('/video/view_video')

@login_required(login_url='/teacher/teacher_signIn' or "admin_login")
def notifications(request):
    post = Post.objects.all()
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    return render(request, 'post/notifications.html', {'notifications': notifications ,"post":post} )



@login_required(login_url=admin_login)
def admin_create_video_form(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if 'image' in request.FILES:
                post.image = request.FILES['image']
            if 'video' in request.FILES:
                post.video = request.FILES['video']
            post.save()
            return redirect("/admin_video")
    else:
        form = PostForm()
    return render(request, 'post/create_video_form.html', {'form': form})

@login_required(login_url=admin_login)
def admin_update_video_form(request ,pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/video/admin_view_video')
    return render(request, 'post/update_video_form.html', {'form': form})


@login_required(login_url=admin_login)
def admin_delete_video_form(request,pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('/video/admin_view_video')

@login_required(login_url=admin_login)
def admin_view_video(request):
    video = Post.objects.all()
    
    return render(request, 'post/view_video.html', {"video":video})


  
