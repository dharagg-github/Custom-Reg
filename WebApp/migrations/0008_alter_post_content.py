# Generated by Django 4.1.1 on 2022-10-26 13:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("WebApp", "0007_post_draft_alter_post_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
