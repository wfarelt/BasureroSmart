# Generated by Django 5.1.2 on 2024-11-26 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0005_alter_rewardclaim_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='rewards/'),
        ),
        migrations.AlterField(
            model_name='rewardclaim',
            name='code',
            field=models.CharField(default='DeVnV7ipzPLK', max_length=12, unique=True),
        ),
    ]
