# Generated by Django 4.1.7 on 2023-04-16 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_user_userscourses_user_usersmealtype_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscourses',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.semester'),
        ),
    ]
