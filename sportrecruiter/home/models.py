from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEAM', 'Team Member'),
        ('PLAYER', 'Player'),
    )

    # Custom fields
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLAYER')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    # Custom methods for role-based permissions
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    def is_team_member(self):
        return self.role == 'TEAM'

    def is_player(self):
        return self.role == 'PLAYER'

    class Meta:
        db_table = 'home_customuser'  # Specify custom table name for the user model

    def __str__(self):
        return self.username
    
    
# ✅ Extending CustomUser with extra fields
class HomeUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='home_user')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Home User: {self.user.username}"


# Team model (for Featured Teams section)
class Team(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Lakers"
    description = models.TextField()         # e.g., "A brief description..."
    is_featured = models.BooleanField(default=False)  # Only featured teams show on homepage
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    def __str__(self):
        return self.name  # Makes it readable in Django admin
    

class HomeTeam(models.Model):
    team_name = models.CharField(max_length=100)
    team_logo = models.ImageField(upload_to='team_logos/')
    team_bio = models.TextField()
    team_region = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.team_name
    

    

# Tryout model (for Upcoming Tryouts section)
class Tryout(models.Model):
    title = models.CharField(max_length=200)       # e.g., "Basketball Tryout"
    date = models.DateField()                      # e.g., "March 10"
    description = models.TextField()               # e.g., "Open registration..."
    is_active = models.BooleanField(default=True)  # Hide if tryout is over

    def __str__(self):
        return self.title


# Blog model (for Blog section)
class BlogPost(models.Model):
    title = models.CharField(max_length=200)      # e.g., "Tips for Improving Your Game"
    content = models.TextField()                  # e.g., "Read our latest tips..."
    is_featured = models.BooleanField(default=False)  # Only featured posts show on homepage
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
