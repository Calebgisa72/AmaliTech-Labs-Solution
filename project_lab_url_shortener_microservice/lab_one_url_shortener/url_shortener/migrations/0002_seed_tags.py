from django.db import migrations


def create_initial_tags(apps, schema_editor):
    Tag = apps.get_model("url_shortener", "Tag")
    # Use the choices from the model definition directly or hardcode to avoid imports
    TAG_CHOICES = [
        ("Marketing", "Marketing"),
        ("Social", "Social"),
        ("News", "News"),
        ("Blog", "Blog"),
        ("E-Commerce", "E-Commerce"),
        ("Education", "Education"),
        ("Entertainment", "Entertainment"),
        ("Technology", "Technology"),
        ("Other", "Other"),
    ]

    for _, name in TAG_CHOICES:
        Tag.objects.get_or_create(name=name)


def remove_tags(apps, schema_editor):
    Tag = apps.get_model("url_shortener", "Tag")
    Tag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("url_shortener", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_tags, remove_tags),
    ]
