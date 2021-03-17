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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import mylogin.views as v1
import papermanager.views as v2
import papershare.views as v3

urlpatterns = [
    path('admin/', admin.site.urls),
    # my login
    path('traceback', v1.track_errors),
    path('home/', v1.login_view),
    path('mylogin/login/', v1.my_login),
    path('mylogin/register/', v1.register_view),
    path('mylogin/applyreg/', v1.register),
    path('mylogin/logout/', v1.my_logout),
    path('mylogin/admission/', v1.admission_view),
    path('mylogin/admit/', v1.admit),
    # paper manager
    path('library/label', v2.view_label),
    path('library/add-label', v2.add_label),
    path('library/delete-label', v2.delete_label),
    path('library/rename-label', v2.rename_label),
    path('library/', v2.view_paper),
    path('library/add-paper', v2.add_paper),
    path('library/delete-paper', v2.delete_paper),
    path('library/change-label', v2.change_paper_s_label),
    # paper share
    path('share', v3.view_link_list),
    path('share/add-link', v3.add_link),
    path('share/link/id=<str:id_>', v3.view_link),
    path('share/list-link', v3.view_link_list),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
