from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    URLResolver,
    include,
    path,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from base.views import (
    BadRequestErrorView,
    ForbiddenErrorView,
    InternalServerErrorView,
    NotFoundErrorView,
)

handler400 = BadRequestErrorView.as_view()
handler403 = ForbiddenErrorView.as_view()
handler404 = NotFoundErrorView.as_view()
handler500 = InternalServerErrorView.as_view()

urlpatterns: list[URLResolver] = [
    # admin
    path(f'{settings.MAIN_PAGE}/admin/' if settings.MAIN_PAGE else 'admin/', admin.site.urls),

    # base
    path(f'{settings.MAIN_PAGE}/' if settings.MAIN_PAGE else '', include('signals.urls')),
    path(f'{settings.MAIN_PAGE}/datasources' if settings.MAIN_PAGE else 'datasources', include('datasources.urls')),

    # debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),

    # sphinx docs
    path(f'{settings.MAIN_PAGE}/docs/' if settings.MAIN_PAGE else 'docs/', include('docs.urls')),

    # drf-spectacular
    path(
        f'{settings.MAIN_PAGE}/api/docs/schema/' if settings.MAIN_PAGE else 'api/docs/schema/',
        SpectacularAPIView.as_view(), name="spectacular-schema"
    ),
    path(
        f'{settings.MAIN_PAGE}/api/docs/swagger/' if settings.MAIN_PAGE else 'api/docs/swagger/',
        SpectacularSwaggerView.as_view(url_name="spectacular-schema"), name="swagger"
    ),
    path(
        f'{settings.MAIN_PAGE}/api/docs/redoc/' if settings.MAIN_PAGE else 'api/docs/redoc/',
        SpectacularRedocView.as_view(url_name="spectacular-schema"), name="redoc"
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
