# Generated by Django 4.1.1 on 2022-10-25 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WebApp", "0004_post_summary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="summary",
            field=models.TextField(),
        ),
    ]
