# Generated by Django 5.2 on 2025-05-02 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_goal_auto_calculate_goal_is_parent_goal_goal_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='kategorie',
            field=models.CharField(choices=[('Gesundheit', 'Gesundheit'), ('Finanzen', 'Finanzen'), ('Karriere', 'Karriere'), ('Lernen', 'Lernen'), ('Sonstiges', 'Sonstiges')]),
        ),
    ]
