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
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import UserSignup

from .forms import LoginForm
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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # 🎯 Role-based redirect
                if user.role == 'PLAYER':
                    return redirect('player')  # Make sure this URL name exists
                elif user.role == 'TEAM':
                    return redirect('team')  # Make sure this URL name exists
                else:
                    return redirect('default_dashboard')  # Just in case

            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'home/auth/login.html', {'form': form})

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
            return redirect('home/login')
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


# --- SIGN UP ---

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Save to DB
        UserSignup.objects.create(username=username, email=email, password=password)
        return redirect('login')  # or wherever you wanna redirect

    return render(request, 'home/auth/register.html')


# --- PLAYER DASHBOARD ---

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('player')  # or wherever you want to go after saving
    else:
        form = EditProfileForm(instance=user)
    
    return render(request, 'home/dashboard/player.html', {'form': form})



from .models import CustomUser
from .forms import EditProfileForm
def update_profile(request):
    user = CustomUser.objects.get(id=request.user.id)  # Assuming the user is logged in

    if request.method == "POST":
        # Check if data is received correctly
        print(request.POST)  # Print out form data

        # Get data from form and bind it to the instance of the current user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.bio = request.POST['bio']

        # Handle Profile Picture Update
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']

        # Save changes
        try:
            user.save()
            print("User data saved successfully!")
        except Exception as e:
            print(f"Error saving user: {e}")

        return redirect('player')  # Redirect to profile view page or another page
    
    return render(request, 'home/dashboard/player.html')  # Your profile edit template
