from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("donors/", views.donor_list, name="donor_list"),
    path("requests/", views.request_list, name="request_list"),
    # path('register/', views.register, name='register'),
   
    path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),  # you can add login later
    path('login/', views.login, name='login'),
    path('become-donor/', views.become_donor, name='become_donor'),
    path('requestor/', views.requestor, name='Requestor'),
    # path("my-requests/", views.my_requests, name="my_requests"),
   
    path("my-requests/", views.my_requests, name="my_requests"),
     path("donor/<str:name>/", views.donor_detail, name="donor_detail"),
     path('logout/', views.logout_view, name='logout'),
     path('about_us/',views.about_us, name='about_us'),

]






   

    

