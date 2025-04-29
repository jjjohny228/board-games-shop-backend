from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

class PingView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "hello world"})


urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
    path("admin/", admin.site.urls),
    path("api/", include('games.urls', namespace="games")),
                  path("schema/", SpectacularAPIView.as_view(), name="schema"),  # JSON схема API
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),  # Swagger UI
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # Redoc UI
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

