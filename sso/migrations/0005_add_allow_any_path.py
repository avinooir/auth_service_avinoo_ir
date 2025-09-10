# Generated manually for adding allow_any_path field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0004_add_allowed_redirect_uris'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssoclient',
            name='allow_any_path',
            field=models.BooleanField(
                default=False,
                help_text='اگر فعال باشد، هر مسیری روی دامنه این کلاینت مجاز است',
                verbose_name='اجازه هر مسیر'
            ),
        ),
    ]
