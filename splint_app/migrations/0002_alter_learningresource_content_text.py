# Generated by Django 4.2.13 on 2025-05-30 12:19

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('splint_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningresource',
            name='content_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='圖文教材內容 (可包含圖片)', null=True),
        ),
    ]
