"""ClixoveLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from .constant import traceback
import mylogin.views as v1
import papermanager.views as v2
import papershare.views as v3

urlpatterns = [
    path('admin/', admin.site.urls),
    # traceback
    path('traceback/<str:guidance>/<str:retrieve>', traceback),
    # mylogin
    path('home/', v1.login_view),
    path('mylogin/login/', v1.mylogin),
    path('mylogin/register/', v1.register_view),
    path('mylogin/applyreg/', v1.register),
    path('mylogin/logout/', v1.mylogout),
    path('mylogin/waitlist/', v1.waitlist_view),
    path('mylogin/admit/', v1.admit),
    # papermanager
    path('library/', v2.library_view),
    path('library/add-paper', v2.add_paper),
    path('library/change-paper', v2.change_papers),
    path('library/projects', v2.labels_view),
    path('library/add-project', v2.add_label),
    path('library/delete-project', v2.delete_label),
    # papershare
    path('share', v3.shared_link_view),
    path('share/share-user-search', v3.shared_user_search),
    path('share/change-links', v3.delete_label),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
