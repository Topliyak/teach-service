# Generated by Django 4.2.3 on 2023-08-14 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_section_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.section'),
        ),
    ]
