from django.contrib import admin

from django.urls import include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/v1/', include('users.urls')),
    re_path(r'^api/v1/', include('articles.urls')),
    re_path(r'^api/v1/', include('tags.urls'))
]
