# Data migration: ensure the default Site record points to the production domain.
# This runs automatically on deploy, so the sitemap framework has the correct
# domain available without needing manual shell intervention on each environment.

from django.db import migrations


def set_default_site(apps, schema_editor):
    # Use apps.get_model rather than importing Site directly. This makes the
    # migration future-proof if the Site model schema ever changes in Django.
    Site = apps.get_model('sites', 'Site')

    # update_or_create handles both fresh databases (creates the record)
    # and existing databases that still have Django's example.com placeholder
    # (updates the record). Either way the result is the same.
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'sweetpeahomehelp.co.uk',
            'name': 'Sweet Pea Home Help',
        },
    )


def revert_default_site(apps, schema_editor):
    # Reversing the migration restores Django's default placeholder.
    # This is rarely needed but Django expects a reverse function for completeness.
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'example.com',
            'name': 'example.com',
        },
    )


class Migration(migrations.Migration):

    # Depends on the sites framework being migrated, plus this app's previous migration
    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('SweetPeaApp', '0004_resourcedocument'),
    ]

    operations = [
        migrations.RunPython(set_default_site, revert_default_site),
    ]