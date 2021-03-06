# Generated by Django 3.0.8 on 2020-07-19 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mini_wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('withdrawn_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('reference_id', models.UUIDField(unique=True)),
                ('withdrawn_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('enabled_at', models.DateTimeField()),
                ('disabled_at', models.DateTimeField()),
                ('balance', models.IntegerField(default=0)),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('deposited_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('reference_id', models.UUIDField(unique=True)),
                ('deposited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
