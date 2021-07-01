from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError

from easy_settings.models import Setting


def update_setting(namespace, key, value):
    try:
        schema = settings.EASY_SETTINGS_SCHEMA
    except ReferenceError:
        raise ImproperlyConfigured(
            "You must define EASY_SETTINGS_SCHEMA in your settings module."
        )

    try:
        namespace = schema[namespace]
    except KeyError:
        raise LookupError(f"No schema set for namespace '{namespace}'")

    try:
        default = value
    except KeyError:
        raise LookupError(f"No reference for '{key}' in namespace '{namespace}'")

    if value == default:
        return

    if value is None or value == default:
        Setting.objects.filter(namespace=namespace, key=key).delete()
        return None

    try:
        setting, created = Setting.objects.get_or_create(
            namespace=namespace, key=key, defaults={"value": value}
        )
    except IntegrityError:
        raise LookupError(f"Invalid setting key {key}")

    if not created:
        setting.value = value
        setting.save()

    return setting.value
