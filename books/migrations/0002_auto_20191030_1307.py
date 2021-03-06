# Generated by Django 2.0 on 2019-10-30 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=' Use pen name,not Real name', max_length=70, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(help_text=' Use pen name,not Real name', max_length=70),
        ),
        migrations.AlterField(
            model_name='book',
            name='is_favourite',
            field=models.BooleanField(default=False, verbose_name='Favourite?'),
        ),
    ]
