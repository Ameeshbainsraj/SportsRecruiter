# home/urls.py
from django.urls import path
from.views import login_view,admin_dashboard_main,team_dashboard_main,player_dashboard_main, homepage, team_profile_view,schedule_tryouts,view_tryouts, signup_view,signup_view_main,register_view, upload_performance,update_profile
urlpatterns = [
    path('home', homepage, name='home'),
    path('login/', login_view, name='login'),

    path('signup/', signup_view, name='signup-view'),
    path('home/admin/', admin_dashboard_main, name='admin'),
    path('home/team/', team_dashboard_main, name='team'),
    path('home/player/', player_dashboard_main, name='player'),
    path('update-team-profile/', team_profile_view, name='update_team_profile'),
    path('schedule-tryouts/', schedule_tryouts, name='schedule-tryouts'),
    path('view-tryouts/', view_tryouts, name='view-tryouts'),
    path('register/', register_view, name='register'),
    path('player/performance/', upload_performance, name='upload-performance'),
    path('player/profile/', update_profile, name='update-profile'),

]
