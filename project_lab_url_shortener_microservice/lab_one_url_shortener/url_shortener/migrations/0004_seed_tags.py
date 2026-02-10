from django.db import migrations


def seed_tags(apps, schema_editor):
    Tag = apps.get_model("url_shortener", "Tag")
    TAG_CATEGORIES = [
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

    for value, label in TAG_CATEGORIES:
        if not Tag.objects.filter(name=label).exists():
            Tag.objects.create(name=label)


class Migration(migrations.Migration):

    dependencies = [
        ("url_shortener", "0003_remove_url_url_shorten_short_c_49214d_idx_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_tags),
    ]
