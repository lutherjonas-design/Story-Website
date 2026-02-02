from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("story", "0003_alter_dictionary_word_alter_wordstoadd_word"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="Dictionary"),
                migrations.DeleteModel(name="WordsToAdd"),
            ],
        ),
    ]