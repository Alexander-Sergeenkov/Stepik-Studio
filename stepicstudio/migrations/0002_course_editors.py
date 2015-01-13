# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stepicstudio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='editors',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
