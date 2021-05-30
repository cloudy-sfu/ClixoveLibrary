from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import my_login.views as v1
import library.views as v2

urlpatterns = [
    path('admin/', admin.site.urls),
    # my login
    path('main', v1.view_login),
    path('my_login/login', v1.add_login),
    path('my_login/quit', v1.delete_login),
    path('my_login/register', v1.view_register),
    path('my_login/register/add', v1.add_register),
    # library
    path('library', v2.view_library),
    path('library/paper/add', v2.add_paper),
    path('library/paper/delete', v2.delete_paper),
    path('library/label', v2.view_label),
    path('library/label/add', v2.add_label),
    path('library/label/delete', v2.delete_label),
    path('library/label/rename/<int:label_id>', v2.rename_label),
    path('library/label_in_paper/add', v2.add_label_paper),
    path('library/label_in_paper/delete', v2.delete_label_paper),
    path('library/label_in_paper/change', v2.change_label_paper),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
