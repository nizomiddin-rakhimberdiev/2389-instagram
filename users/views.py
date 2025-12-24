from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Chat, Message
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html')

def profile_view(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'profile.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(username=username, email=email, phone=phone, password=password)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')


@login_required
def inbox(request):
    chats = Chat.objects.filter(participants=request.user).order_by("-updated_at")
    return render(request, "inbox.html", {"chats": chats})


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(CustomUser, username=username)

    # O'zingga yozishni oldini olamiz
    if other_user == request.user:
        return redirect("profile", username=username)

    # Oldindan chat bormi tekshiramiz
    chat = Chat.objects.filter(participants=request.user)\
                       .filter(participants=other_user)\
                       .first()

    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)

    return redirect("chat_detail", chat_id=chat.id)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.all().order_by("created_at")

    return render(request, "chat_detail.html", {
        "chat": chat,
        "messages": messages
    })
