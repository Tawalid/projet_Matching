# Generated by Django 3.1.1 on 2020-10-09 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=15)),
                ('portable', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('formation', models.CharField(max_length=100000)),
                ('experiences1', models.CharField(max_length=100000)),
                ('experiences2', models.CharField(max_length=100000)),
                ('experiences3', models.CharField(max_length=100000)),
                ('competences', models.CharField(max_length=100000)),
                ('divers', models.CharField(max_length=1000)),
                ('linkedin', models.CharField(max_length=1000)),
                ('CV', models.FileField(upload_to='media/pdf')),
                ('sexe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.position')),
            ],
        ),
    ]