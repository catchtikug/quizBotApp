# Generated by Django 5.2.1 on 2025-05-17 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '2. Categories',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.categories')),
            ],
            options={
                'verbose_name_plural': '3. Books',
            },
        ),
        migrations.CreateModel(
            name='Chapters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_number', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.books')),
            ],
            options={
                'verbose_name_plural': '4. Chapters',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('correct_answer', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.books')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapters')),
            ],
            options={
                'verbose_name_plural': '6. Questions',
            },
        ),
        migrations.CreateModel(
            name='QuestionOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.questions')),
            ],
            options={
                'verbose_name_plural': '7. QuestionOptions',
            },
        ),
        migrations.CreateModel(
            name='Verses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verse_number', models.IntegerField(default=0)),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.books')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapters')),
            ],
            options={
                'verbose_name_plural': '5. Verses',
            },
        ),
        migrations.AddField(
            model_name='questions',
            name='verse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.verses'),
        ),
    ]
