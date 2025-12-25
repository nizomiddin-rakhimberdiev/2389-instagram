from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='login')
def home_page(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)

@login_required
def search_users(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        users = list(
            CustomUser.objects.filter(username__icontains=query)
            .values("username", 'avatar', "id")
        )
    for user in users:
            results.append({
                "username": user["username"],
                "avatar": request.build_absolute_uri(user['avatar']),
            })

    return JsonResponse({"results": users})


@login_required(login_url='login')
def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        post = Post.objects.get(id=post_id)
        Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        return redirect('home')
    return render(request, 'index.html')

@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        title = request.POST.get("title")

        Post.objects.create(
            author=request.user,
            image=image,
            video=video,
            title=title
        )
        return redirect("home")

    return render(request, "create_post.html")


@login_required(login_url='login')
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by("created_at")

    if request.method == "POST":
        Comment.objects.create(
            post=post,
            author=request.user,
            content=request.POST.get("text")
        )
        return redirect("post_detail", post_id=post.id)

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments
    })
