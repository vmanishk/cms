# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.batch'
        db.add_column(u'cmsdata_userprofile', 'batch',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.batch'
        db.delete_column(u'cmsdata_userprofile', 'batch_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cmsdata.course': {
            'Course_Name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Course_Number': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'Course_Prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Course_Prerequisites_rel_+'", 'null': 'True', 'to': u"orm['cmsdata.Course']"}),
            'Course_Students': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True'}),
            'Course_Teachers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'Elective': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.material': {
            'Material_Course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsdata.Course']"}),
            'Material_Gist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Material_Link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'Meta': {'object_name': 'Material'},
            'Thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'Student_Status_PorF': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'if_first_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'cmsdata.usertocalender': {
            'Event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_bootstrap_calendar.CalendarEvent']"}),
            'Event_Creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'Meta': {'object_name': 'UserToCalender'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.votingtopic': {
            'Meta': {'object_name': 'VotingTopic'},
            'Topic_Count_No': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Topic_Count_Yes': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Topic_Creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'Topic_End_Date': ('django.db.models.fields.DateField', [], {'max_length': '11'}),
            'Topic_Name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'Topic_Start_Date': ('django.db.models.fields.DateField', [], {'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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

    complete_apps = ['cmsdata']