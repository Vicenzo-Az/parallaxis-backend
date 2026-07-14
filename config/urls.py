from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth (simplejwt padrão — RF02, RF03)
    path("api/auth/token/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("api/auth/token/refresh/",
         TokenRefreshView.as_view(), name="token_refresh"),
    # Bounded contexts
    path("api/users/", include("apps.users.api.urls")),
    path("api/", include("apps.games.api.urls")),
    # Documentação OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
