# Generated by Django 2.0 on 2019-10-30 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20191030_1307'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Authour',
            new_name='Author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='books', to='books.Author'),
        ),
    ]