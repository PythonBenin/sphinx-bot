# Generated by Django 2.2.7 on 2019-11-29 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20191123_1327'),
        ('repository', '0003_auto_20191123_2215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repository',
            old_name='github_user',
            new_name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='repository',
            unique_together={('github_id', 'owner')},
        ),
    ]
