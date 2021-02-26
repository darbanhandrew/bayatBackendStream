# Generated by Django 3.1.7 on 2021-02-26 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oneTime.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logged_in_before', models.BooleanField(default=False)),
                ('stream_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('ip', models.CharField(blank=True, max_length=100, null=True)),
                ('jti', models.CharField(default=oneTime.utils.generate_jti, editable=False, help_text='JWT tokens for the user get revoked when JWT id has regenerated.', max_length=64, verbose_name='jwt id')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
