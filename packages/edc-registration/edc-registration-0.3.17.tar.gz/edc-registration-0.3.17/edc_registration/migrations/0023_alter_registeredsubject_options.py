# Generated by Django 3.2.11 on 2022-04-12 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_registration', '0022_auto_20210801_2021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registeredsubject',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'export', 'import'), 'get_latest_by': 'modified', 'ordering': ['subject_identifier'], 'permissions': (('display_firstname', 'Can display first name'), ('display_lastname', 'Can display last name'), ('display_dob', 'Can display DOB'), ('display_identity', 'Can display identity number'), ('display_initials', 'Can display initials')), 'verbose_name': 'Registered Subject', 'verbose_name_plural': 'Registered Subjects'},
        ),
    ]
