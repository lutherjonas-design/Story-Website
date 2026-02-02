from django.db import migrations

def move_ct_permissions(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")

    for model in ("dictionary", "wordstoadd"):
        try:
            old_ct = ContentType.objects.get(app_label="story", model=model)
        except ContentType.DoesNotExist:
            old_ct = None

        # Ensure target exists
        new_ct, _ = ContentType.objects.get_or_create(app_label="dictionary", model=model)

        if old_ct:
            # Repoint any permissions bound to the old content type
            Permission.objects.filter(content_type=old_ct).update(content_type=new_ct)
            # Remove the old content type to avoid duplicates
            old_ct.delete()

class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0001_adopt_existing_dictionary_tables"),
        ("contenttypes", "0002_remove_content_type_name"),  # Safe baseline
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(move_ct_permissions, migrations.RunPython.noop),
    ]
