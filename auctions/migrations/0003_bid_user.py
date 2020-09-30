# Generated by Django 3.1.1 on 2020-09-30 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200930_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='auctions.user'),
            preserve_default=False,
        ),
    ]
