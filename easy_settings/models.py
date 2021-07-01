from django.db import models


class Setting(models.Model):
    class Meta:
        db_table = "settings"
        constraints = [
            models.UniqueConstraint(
                fields=["namespace", "reference", "key"],
                name="unique_key_per_user_per_namespace",
            )
        ]

    namespace = models.CharField(
        max_length=100,
        help_text="If you wanted settings for two different entities (e.g: Settings for Users and settings for how "
        "invoices are laid out) you can distinguish them here.",
    )
    reference = models.CharField(
        max_length=100,
        help_text="The object that the settings apply to (e.g: An individual user).",
    )
    key = models.CharField(
        max_length=100,
        help_text="The namespace-specific reference for the setting (e.g: is_dark_mode_enabled)",
    )
    value = models.CharField(
        max_length=1000, help_text="The value of the setting (e.g: 'True')."
    )
