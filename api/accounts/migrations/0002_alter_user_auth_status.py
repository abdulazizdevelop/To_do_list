# Generated by Django 5.1.3 on 2024-12-18 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_status',
            field=models.CharField(choices=[('sentemail', 'Sent_email'), ('verify_code', 'Verify_code'), ('complete', 'Complete')], default='sentemail', max_length=25),
        ),
    ]
