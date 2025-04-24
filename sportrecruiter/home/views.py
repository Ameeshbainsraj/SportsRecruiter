from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SignupForm, TryoutForm
from .models import Team, Tryout, BlogPost
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# --- Main Views ---
def login_view_main(request):
    return render(request, 'home/auth/login.html')

def signup_view_main(request):
    return render(request, 'home/auth/signup.html')

def admin_dashboard_main(request):
    return render(request, 'home/dashboard/admin.html')

def team_dashboard_main(request):
    return render(request, 'home/dashboard/team.html')

def player_dashboard_main(request):
    return render(request, 'home/dashboard/player.html')

# --- Authentication Views ---
def login_view(request):
    """Login view that handles user authentication."""
    if request.user.is_authenticated:
        return redirect_to_dashboard(request.user)

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_to_dashboard(user)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set additional fields
            user.role = form.cleaned_data['role']
            user.save()
            
            # This line is needed for proper password hashing
            form.save_m2m()  
            
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            # Pass form errors to template
            messages.error(request, "Please correct the errors below.")
            return render(request, 'home/auth/signup.html', {'form': form})
    else:
        form = SignupForm()
    
    return render(request, 'home/auth/signup.html', {'form': form})


# --- Team Profile View ---
def team_profile_view(request, team_id=None):
    """View to create or edit a team profile."""
    team = get_object_or_404(Team, id=team_id) if team_id else None

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_featured = request.POST.get('is_featured') == 'on'
        logo = request.FILES.get('logo')

        if name and description:
            if team:
                team.name = name
                team.description = description
                team.is_featured = is_featured
                if logo:
                    team.logo = logo
                team.save()
                messages.success(request, "Team updated successfully!")
            else:
                Team.objects.create(
                    name=name,
                    description=description,
                    is_featured=is_featured,
                    logo=logo
                )
                messages.success(request, "Team created successfully!")
        else:
            messages.error(request, "Name and Description are required!")

    context = {'team': team}
    return render(request, 'home/dashboard/team.html', context)

# --- Homepage Views ---
def homepage_view(request):
    """Displays featured teams on the homepage."""
    featured_teams = Team.objects.filter(is_featured=True)
    return render(request, 'home/index.html', {'teams': featured_teams})

def homepage(request):
    """Fetch featured teams, tryouts, and blog posts for the homepage."""
    featured_teams = Team.objects.filter(is_featured=True)
    upcoming_tryouts = Tryout.objects.filter(is_active=True)
    featured_blog_posts = BlogPost.objects.filter(is_featured=True)

    context = {
        'featured_teams': featured_teams,
        'upcoming_tryouts': upcoming_tryouts,
        'featured_blog_posts': featured_blog_posts,
    }
    return render(request, 'home/index.html', context)

# --- Tryouts Views ---
def schedule_tryouts(request):
    """Schedule a new tryout."""
    if request.method == 'POST':
        form = TryoutForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'home/dashboard/team.html', {
                'form': TryoutForm(),  # Reset the form
                'message': '✅ Tryout created successfully!'
            })
    else:
        form = TryoutForm()

    return render(request, 'home/dashboard/team.html', {'form': form})

def view_tryouts(request):
    """View all upcoming tryouts."""
    tryouts = Tryout.objects.all()
    return render(request, 'home/dashboard/team.html', {'tryouts': tryouts})

# --- Logout & Redirect Views ---
def logout_view(request):
    """Log out the user."""
    logout(request)
    return redirect('home')

def redirect_to_dashboard(user):
    """Redirect users based on their role."""
    if user.is_admin():
        return redirect('admin_dashboard')
    elif user.is_team_member():
        return redirect('team_dashboard')
    else:
        return redirect('player_dashboard')

# --- Dashboard Views ---
@login_required
def admin_dashboard(request):
    """Admin dashboard accessible only by admin users."""
    if not request.user.is_admin():
        return redirect('home')
    return render(request, 'dashboard/admin.html')

@login_required
def team_dashboard(request):
    """Team dashboard accessible only by team members."""
    if not request.user.is_team_member():
        return redirect('home')
    return render(request, 'dashboard/team.html')

@login_required
def player_dashboard(request):
    """Player dashboard accessible only by players."""
    if not request.user.is_player():
        return redirect('home')
    return render(request, 'dashboard/player.html')

# --- Search Views ---
def search(request):
    """Search for teams, tryouts, and blog posts."""
    query = request.GET.get('q', '')
    teams = Team.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    tryouts = Tryout.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )
    blogposts = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    )

    context = {
        'teams': teams,
        'tryouts': tryouts,
        'blogposts': blogposts,
        'query': query,
    }
    return render(request, 'home/search.html', context)