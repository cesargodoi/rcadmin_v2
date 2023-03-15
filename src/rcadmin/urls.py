from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

# from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("user/", include("apps.user.urls")),
    path("", include("apps.base.urls")),
    path("center/", include("apps.center.urls")),
    path("person/", include("apps.person.urls")),
    path("workgroup/", include("apps.workgroup.urls")),
    path("event/", include("apps.event.urls")),
    path("treasury/", include("apps.treasury.urls")),
    path("publicwork/", include("apps.publicwork.urls")),
    path("presidium/", include("apps.presidium.urls")),
]

handler404 = "apps.base.views.base.error_404"
handler500 = "apps.base.views.base.error_500"

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r"^rosetta/", include("rosetta.urls")),
    ]
