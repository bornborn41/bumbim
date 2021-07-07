from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path('djrichtextfield/', include('djrichtextfield.urls')),
    # app
    path('', views.HomeView.as_view(), name='login'),
    path('edit/<int:pk>/', views.EditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('total/', views.TotalView.as_view(), name='total'),
    path('test/', views.TestView.as_view(), name='test'),

    # auth
    path('logout/', views.logout_views, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<str:username>/',
         views.EditProfileView.as_view(), name='editprofile'),

]
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
