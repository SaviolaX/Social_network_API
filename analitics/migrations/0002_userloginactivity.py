# Generated by Django 4.0 on 2021-12-20 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userloginactivity'),
        ('analitics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoginActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(db_index=True, max_length=40)),
                ('login', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Logged_in_user', to='users.user')),
            ],
            options={
                'verbose_name_plural': 'user login activities',
            },
        ),
    ]
