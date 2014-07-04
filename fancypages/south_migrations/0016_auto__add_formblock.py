# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormBlock'
        db.create_table(u'fancypages_formblock', (
            (u'contentblock_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fancypages.ContentBlock'], unique=True, primary_key=True)),
            ('form_selection', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'fancypages', ['FormBlock'])


    def backwards(self, orm):
        # Deleting model 'FormBlock'
        db.delete_table(u'fancypages_formblock')


    models = {
        u'assets.imageasset': {
            'Meta': {'object_name': 'ImageAsset'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('shortuuidfield.fields.ShortUUIDField', [], {'db_index': 'True', 'max_length': '22', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fancypages.carouselblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'CarouselBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_1': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_10': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_2': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_3': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_4': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_5': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_6': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_7': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_8': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'image_9': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'link_url_1': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_10': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_2': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_3': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_4': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_5': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_6': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_7': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_8': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'link_url_9': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.container': {
            'Meta': {'unique_together': "(('name', 'content_type', 'object_id', 'language_code'),)", 'object_name': 'Container'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "u'en-us'", 'max_length': '7'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'uuid': ('shortuuidfield.fields.ShortUUIDField', [], {'db_index': 'True', 'max_length': '22', 'blank': 'True'})
        },
        u'fancypages.contentblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'ContentBlock'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blocks'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('shortuuidfield.fields.ShortUUIDField', [], {'db_index': 'True', 'max_length': '22', 'blank': 'True'})
        },
        'fancypages.fancypage': {
            'Meta': {'object_name': 'FancyPage'},
            'date_visible_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_visible_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pages'", 'symmetrical': 'False', 'to': "orm['fancypages.PageGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'page'", 'unique': 'True', 'null': 'True', 'to': "orm['fancypages.PageNode']"}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['fancypages.PageType']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'uuid': ('shortuuidfield.fields.ShortUUIDField', [], {'db_index': 'True', 'max_length': '22', 'blank': 'True'})
        },
        u'fancypages.formblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'FormBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'form_selection': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'fancypages.fourcolumnlayoutblock': {
            'Meta': {'object_name': 'FourColumnLayoutBlock'},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.horizontalseparatorblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'HorizontalSeparatorBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'fancypages.imageandtextblock': {
            'Meta': {'object_name': 'ImageAndTextBlock', '_ormbases': [u'fancypages.ContentBlock']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "u'image_text_blocks'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u'Your text goes here.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'fancypages.imageblock': {
            'Meta': {'object_name': 'ImageBlock', '_ormbases': [u'fancypages.ContentBlock']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "u'image_blocks'", 'null': 'True', 'to': u"orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.orderedcontainer': {
            'Meta': {'object_name': 'OrderedContainer', '_ormbases': ['fancypages.Container']},
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'fancypages.pagegroup': {
            'Meta': {'object_name': 'PageGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'uuid': ('shortuuidfield.fields.ShortUUIDField', [], {'db_index': 'True', 'max_length': '22', 'blank': 'True'})
        },
        u'fancypages.pagenavigationblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'PageNavigationBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'origin': ('django.db.models.fields.CharField', [], {'default': "u'absolute'", 'max_length': '50'})
        },
        'fancypages.pagenode': {
            'Meta': {'object_name': 'PageNode'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'fancypages.pagetype': {
            'Meta': {'object_name': 'PageType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('shortuuidfield.fields.ShortUUIDField', [], {'db_index': 'True', 'max_length': '22', 'blank': 'True'})
        },
        'fancypages.tabblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'TabBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'fancypages.textblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'TextBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u'Your text goes here.'"})
        },
        'fancypages.threecolumnlayoutblock': {
            'Meta': {'object_name': 'ThreeColumnLayoutBlock'},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'fancypages.titletextblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'TitleTextBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u'Your text goes here.'"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Your title goes here.'", 'max_length': '100'})
        },
        'fancypages.twitterblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'TwitterBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'max_tweets': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fancypages.twocolumnlayoutblock': {
            'Meta': {'object_name': 'TwoColumnLayoutBlock'},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'left_width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6', 'max_length': '3'})
        },
        'fancypages.videoblock': {
            'Meta': {'ordering': "[u'display_order']", 'object_name': 'VideoBlock', '_ormbases': [u'fancypages.ContentBlock']},
            u'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video_code': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['fancypages']