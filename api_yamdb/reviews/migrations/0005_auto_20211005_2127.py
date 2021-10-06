# Generated by Django 2.2.16 on 2021-10-05 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20211005_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to='reviews.Review'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='title_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_id_reviews', to='reviews.Title'),
        ),
    ]