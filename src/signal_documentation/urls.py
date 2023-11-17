from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    URLResolver,
    include,
    path,
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
    path(f'{settings.MAIN_PAGE}/admin/' if settings.MAIN_PAGE else 'admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path(f'{settings.MAIN_PAGE}/' if settings.MAIN_PAGE else '', include('signals.urls')),
    path(f'{settings.MAIN_PAGE}/docs/' if settings.MAIN_PAGE else 'docs/', include('docs.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
