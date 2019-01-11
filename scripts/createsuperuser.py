#!/usr/bin/env python

import django
django.setup()
from django.contrib.auth.management.commands.createsuperuser import get_user_model

get_user_model()._default_manager.db_manager('default').create_superuser( username='admin', email='a@a.com', password='F1b3rc0rp')