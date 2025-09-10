# Generated manually for adding allowed_redirect_uris field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0003_alter_ssosession_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssoclient',
            name='allowed_redirect_uris',
            field=models.JSONField(
                blank=True, 
                default=list, 
                help_text='لیست آدرس\u200cهای بازگشت مجاز برای این کلاینت', 
                verbose_name='آدرس\u200cهای بازگشت مجاز'
            ),
        ),
    ]
