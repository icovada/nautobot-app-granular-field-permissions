"""Django urlpatterns declaration for granular_field_permissions app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter


from granular_field_permissions import views


app_name = "granular_field_permissions"
router = NautobotUIViewSetRouter()

# The standard is for the route to be the hyphenated version of the model class name plural.
# for example, ExampleModel would be example-models.
router.register("granular-field-permissions-example-models", views.GranularFieldPermissionsExampleModelUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("granular_field_permissions/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
