from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('',views.homepage_view,name="home"),
    path('codeeditor/',views.chatbot,name="codeeditor"),
    path('complexity/', views.complexity_bot, name='complexity_bot'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.note_detail, name='note_detail'),
    path('addnote/', views.add_note, name='add_note'),
    path('signup/', views.signup, name='signup'),
    path('problem_list',views.problem_list, name='problem_list'),  # URL to view the list of problems
    path('compile/<int:problem_id>/', views.compile_and_execute, name='compile_page'),  # URL for the compile page
]
