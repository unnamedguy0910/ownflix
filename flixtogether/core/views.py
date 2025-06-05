from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Room, Video, Message
from django.http import JsonResponse


def home(request):
    return render(request, 'core/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:home')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home')


from django.utils.text import slugify
import uuid

@login_required
def create_room(request):
    if request.method == 'POST':
        slug = request.POST.get('room_slug')
        if slug:
            slug = slugify(slug)
            if Room.objects.filter(slug=slug).exists():
                return render(request, 'core/home.html', {'error': 'Room slug already exists'})
        else:
            return render(request, 'core/home.html', {'error': 'Slug cannot be empty'})
    else:
        # If GET request, create room with random slug
        slug = str(uuid.uuid4())[:8]
    room = Room.objects.create(slug=slug, created_by=request.user)
    return redirect('core:room', room_slug=slug)



@login_required
def join_room(request):
    slug = request.GET.get('room_slug')
    if slug:
        if Room.objects.filter(slug=slug).exists():
            return redirect('room', room_slug=slug)
        else:
            return render(request, 'core/home.html', {'error': 'Room not found'})
    return redirect('core:home')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Room, Message, Video

@login_required
def room_view(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    video = Video.objects.filter(room=room).first()

    return render(request, 'core/room.html', {
        'room': room,
        'messages': messages,
        'video': video,
        'youtube_url': room.youtube_url,
        'user': request.user,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room, Message

@login_required
def profile_view(request):
    user = request.user

    # Rooms the user created
    created_rooms = Room.objects.filter(created_by=user)

    # Rooms where the user sent at least one message
    joined_rooms = Room.objects.filter(messages__user=user).distinct()

    return render(request, 'core/profile.html', {
        'created_rooms': created_rooms,
        'joined_rooms': joined_rooms,
    })
