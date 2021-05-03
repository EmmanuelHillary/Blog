from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.template.loader import render_to_string
from .models import Post, PostImage, Comment
from .forms import PostCreateForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, PostImageForm,\
    PostEditForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import os


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise Http404()
    photo = PostImage.objects.filter(post=post)
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        image_form = PostImageForm(request.POST, request.FILES, photo.all())
        files = request.FILES.getlist('image')
        if form.is_valid() and image_form.is_valid():
            post = form.save(commit=False)
            post.save()
            for f in files:
                file_instance = PostImage(post=post, image=f)
                file_instance.save()
            messages.success(request, f'{ post.title.capitalize() } has been successfully updated!')
            return redirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        image_form = PostImageForm(initial={'image': photo.all()})
    context = {'form': form, 'image_form': image_form, 'photo': photo}
    return render(request, 'blog/post_edit.html', context)


def delete_photo(request, pk):
    photo = get_object_or_404(PostImage, pk=pk)
    post = photo.post
    photo.delete()
    return redirect(post.get_absolute_edit_url())


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise Http404()
    post.delete()
    messages.success(request, 'Posts has been successfully deleted!')
    return redirect('post:list')


@login_required(login_url='post:login')
def favourite_post_list(request):
    user = request.user
    favourite_posts = user.favourites.all()
    context = {
        'favourite_posts': favourite_posts
    }
    return render(request, 'blog/favourites.html', context)


@login_required(login_url='post:login')
def favourite_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.favourite.filter(username=request.user.username).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return redirect(post.get_absolute_url())


@login_required(login_url='post:login')
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_like = False
    if post.likes.filter(username=request.user.username).exists():
        post.likes.remove(request.user)
        is_like = False
    else:
        post.likes.add(request.user)
        is_like = True

    context = {'post': post, 'is_like': is_like, 'total_likes': post.total_likes()}

    if request.is_ajax():
        html = render_to_string('blog/like.html', context, request=request)
        return JsonResponse({'form': html})


@login_required(login_url='login/')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('post:list')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'blog/edit_profile.html', context)


def post_list(request):
    posts = Post.objects.all()
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(body__icontains=query)
        ).distinct()
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    def page_list_generator(post):
        start_ind = 0
        end_ind = 3
        if post.number == paginator.page_range[-1]:
            start_ind = post.number - 3
            end_ind = start_ind + end_ind
        if post.number > 2 and post.number != paginator.page_range[-1]:
            start_ind = post.number - 2
            end_ind = start_ind + end_ind
        return start_ind, end_ind

    if page is None:
        start_index = 0
        end_index = 3

    else:
        start_index, end_index = page_list_generator(posts)

    page_range = list(paginator.page_range)[start_index:end_index]

    context = {'posts': posts, 'query': query, 'page_range': page_range}
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk, slug):
    post = get_object_or_404(Post, pk=pk, slug=slug)
    photos = PostImage.objects.filter(post=post)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    image_many = False
    video = False
    image_one = False
    if photos:
        try:
            photo = PostImage.objects.get(post=post)
            filename = photo.image.name
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.mp4', '.mpg', '.mov', '.ogg']:
                video = True
            elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
                image_one = True
        except:
            image_many = True
    is_like = False
    is_favourite = False

    if post.likes.filter(username=request.user.username).exists():
        is_like = True
    if post.favourite.filter(username=request.user.username).exists():
        is_favourite = True

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            reply_id = request.POST.get('comment_id')
            if reply_id:
                reply = Comment.objects.get(id=reply_id)
                comment.reply = reply
            comment.user = request.user
            comment.post = post
            comment.save()
            # return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    context = {'post': post, 'is_like': is_like, 'is_favourite': is_favourite, 'total_likes': post.total_likes(),
               'photos': photos, 'video': video, 'image_one': image_one, 'image_many': image_many,
               'comments': comments, 'form': form}
    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_detail.html', context)


def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST or None)
        image_form = PostImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and image_form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for f in files:
                file_instance = PostImage(post=post, image=f)
                file_instance.save()
            messages.success(request, 'Posts has been successfully created')
            return redirect(post.get_absolute_url())
    else:
        form = PostCreateForm()
        image_form = PostImageForm()
    context = {'form': form, 'image_form': image_form}
    return render(request, 'blog/post_create.html', context)


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username  = form.cleaned_data.get("username")
            password  = form.cleaned_data.get("password") 
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post:list')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'blog/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('post:login')


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        password = request.POST['password1']
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            return redirect('post:login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'blog/register.html', context)
