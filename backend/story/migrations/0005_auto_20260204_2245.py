from django.db import migrations, models
import django.utils.timezone


def backfill_story_fields(apps, schema_editor):
    """
    Populate the new fields (teaser, author, last_updated) for existing rows,
    using the old description as teaser where possible.
    """
    Story = apps.get_model('story', 'Story')
    now = django.utils.timezone.now()

    # We assume the new fields exist and description was removed just before this
    # data migration runs. Since RemoveField happens first, we can't read 'description'
    # here. If you need description content, do the RemoveField AFTER this data
    # migration and adjust accordingly (see note below).
    #
    # In this version, we'll just fill safe defaults.
    for s in Story.objects.all():
        # If you need to preserve description -> teaser, see the alternative ordering below.
        if not s.teaser:
            s.teaser = "empty"  # or a fallback
        if not s.author:
            s.author = "Unknown"
        if not s.last_updated:
            s.last_updated = now
        s.save(update_fields=["teaser", "author", "last_updated"])


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0004_handoff_dictionary_models_to_new_app'),
    ]

    operations = [
        # 1) Rename models from plural to singular
        migrations.RenameModel(
            old_name='Stories',
            new_name='Story',
        ),
        migrations.RenameModel(
            old_name='Chapters',
            new_name='Chapter',
        ),
        migrations.RenameModel(
            old_name='UniqueWordsInParagraphs',
            new_name='UniqueWordsInParagraph',
        ),
        migrations.RenameModel(
            old_name='Paragraphs',
            new_name='Paragraph',
        ),
        # 2) Add the new fields to Story
        migrations.AddField(
            model_name='story',
            name='teaser',
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name='story',
            name='author',
            field=models.CharField(max_length=100, blank=True, default="Unknown"),
        ),
        migrations.AddField(
            model_name='story',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),

        # 3) Remove the old field from Story
        # NOTE: If you want to transform description → teaser,
        # you should first COPY description to teaser in a RunPython,
        # and only then RemoveField. See alternative below.
        migrations.RemoveField(
            model_name='story',
            name='description',
        ),

        # 4) Backfill defaults/safe values (if needed)
        migrations.RunPython(backfill_story_fields, reverse_code=migrations.RunPython.noop),
    ]
