# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'cmsdata_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Course_Name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('Course_Number', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'cmsdata', ['Course'])

        # Adding M2M table for field Course_Users on 'Course'
        m2m_table_name = db.shorten_name(u'cmsdata_course_Course_Users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'cmsdata.course'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'user_id'])

        # Adding model 'Material'
        db.create_table(u'cmsdata_material', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Material_Gist', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Material_Link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('Material_Course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsdata.Course'])),
        ))
        db.send_create_signal(u'cmsdata', ['Material'])

        # Adding model 'Attendance'
        db.create_table(u'cmsdata_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Todays_Date', self.gf('django.db.models.fields.DateField')(max_length=11)),
            ('Ojas', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('Manish', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('Rohan', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('Deepak', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('Divyansh', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('Attendance_Course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsdata.Course'])),
        ))
        db.send_create_signal(u'cmsdata', ['Attendance'])

        # Adding model 'VotingTopic'
        db.create_table(u'cmsdata_votingtopic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Topic_Name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('Topic_Start_Date', self.gf('django.db.models.fields.DateField')(max_length=11)),
            ('Topic_End_Date', self.gf('django.db.models.fields.DateField')(max_length=11)),
            ('Topic_Count_Yes', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Topic_Count_No', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Topic_Creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'cmsdata', ['VotingTopic'])

        # Adding model 'DiscussionTopic'
        db.create_table(u'cmsdata_discussiontopic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('DiscussionTopic_Name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('DiscussionTopic_Reply', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('DiscussionTopic_Creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'cmsdata', ['DiscussionTopic'])

        # Adding model 'UserToCalender'
        db.create_table(u'cmsdata_usertocalender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Event_Creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('Event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_bootstrap_calendar.CalendarEvent'])),
        ))
        db.send_create_signal(u'cmsdata', ['UserToCalender'])

        # Adding model 'UserProfile'
        db.create_table(u'cmsdata_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('user_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'cmsdata', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'cmsdata_course')

        # Removing M2M table for field Course_Users on 'Course'
        db.delete_table(db.shorten_name(u'cmsdata_course_Course_Users'))

        # Deleting model 'Material'
        db.delete_table(u'cmsdata_material')

        # Deleting model 'Attendance'
        db.delete_table(u'cmsdata_attendance')

        # Deleting model 'VotingTopic'
        db.delete_table(u'cmsdata_votingtopic')

        # Deleting model 'DiscussionTopic'
        db.delete_table(u'cmsdata_discussiontopic')

        # Deleting model 'UserToCalender'
        db.delete_table(u'cmsdata_usertocalender')

        # Deleting model 'UserProfile'
        db.delete_table(u'cmsdata_userprofile')


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
        u'cmsdata.attendance': {
            'Attendance_Course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsdata.Course']"}),
            'Deepak': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Divyansh': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Manish': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Meta': {'object_name': 'Attendance'},
            'Ojas': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Rohan': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Todays_Date': ('django.db.models.fields.DateField', [], {'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.course': {
            'Course_Name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'Course_Number': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'Course_Users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.discussiontopic': {
            'DiscussionTopic_Creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'DiscussionTopic_Name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'DiscussionTopic_Reply': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'Meta': {'object_name': 'DiscussionTopic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.material': {
            'Material_Course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmsdata.Course']"}),
            'Material_Gist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Material_Link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'Meta': {'object_name': 'Material'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cmsdata.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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