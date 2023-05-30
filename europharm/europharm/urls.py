"""europharm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from pharmapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('signin/', signin),
    path('signup/', signup),
    path('admingoi/', adminsignin),
    path('admingoi/admin', admingoi),
    path('admingoi/admin/med/', medicine),
    path('admingoi/admin/users/', users),
    path('admingoi/<int:medicine_id>/', adminupdate),
    path('admingoi/<int:medicine_id>/update/', updatedb),
    path('admingoi/<int:medicine_id>/delete', deleteitem),
    path('admingoi/add/', insertdb),
    path('admingoi/signup/', adminsignup),
    path('adminpage/', signin),
    path('img/', images),
    path('profile/', profile, name="profile"),
    path('profile/<int:pk_id>/', useredit),
    path('profile/<int:pk_id>/edit/', userupdate),
    path('signout/', signout),
    path('admingoi/<int:user_id>/deleteuser', deleteusers),
    path('admingoi/<int:user_id>/edituser', editusers),
    path('<int:item_id>/', itempage, name="itempage"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
