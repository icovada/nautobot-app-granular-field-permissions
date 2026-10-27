"""Runtime generation and registration of Nautobot CustomValidators."""

from nautobot.apps.models import CustomValidator
from nautobot.extras.plugins import register_custom_validators


def build_custom_validator(model: str, clean_func, name: str) -> type[CustomValidator]:
    """Build a `CustomValidator` subclass in memory.

    Args:
        model: Model label in the form `<app_label>.<model_name>`, e.g. `dcim.manufacturer`.
        clean_func: Function taking the validator instance as `self`. The object under validation is
            `self.context["object"]`; raise `ValidationError` (e.g. via `self.validation_error()`) to reject it.
        name: Class name of the generated validator.
    """
    return type(name, (CustomValidator,), {"model": model.lower(), "clean": clean_func, "__module__": __name__})


def _manufacturer_clean(self):
    """Reject Manufacturer names starting with a lowercase letter."""
    obj = self.context["object"]
    if obj.name and obj.name[0].islower():
        self.validation_error({"name": "Manufacturer name must not start with a lowercase letter."})


def register_runtime_validators():
    """Generate and register this app's CustomValidators.

    Nautobot looks up `registry["plugin_custom_validators"]` on every `clean()` call of models with the
    `custom_validators` feature, so validators registered here take effect without a `custom_validators.py` module.
    """
    register_custom_validators(
        [build_custom_validator("dcim.manufacturer", _manufacturer_clean, name="RuntimeManufacturerValidator")]
    )
