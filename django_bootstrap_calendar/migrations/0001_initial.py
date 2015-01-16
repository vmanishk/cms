# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CalendarEvent'
        db.create_table(u'django_bootstrap_calendar_calendarevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('css_class', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'django_bootstrap_calendar', ['CalendarEvent'])


    def backwards(self, orm):
        # Deleting model 'CalendarEvent'
        db.delete_table(u'django_bootstrap_calendar_calendarevent')


    models = {
        u'django_bootstrap_calendar.calendarevent': {
            'Meta': {'object_name': 'CalendarEvent'},
            'css_class': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['django_bootstrap_calendar']