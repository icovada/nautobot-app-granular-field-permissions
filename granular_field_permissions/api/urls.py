"""Django API urlpatterns declaration for granular_field_permissions app."""

from nautobot.apps.api import OrderedDefaultRouter

from granular_field_permissions.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("granular-field-permissions-example-models", views.ContentTypeRuleSetViewSet)

app_name = "granular_field_permissions-api"
urlpatterns = router.urls
