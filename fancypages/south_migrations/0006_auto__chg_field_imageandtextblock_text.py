# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from fancypages.compat import AUTH_USER_MODEL, AUTH_USER_MODEL_NAME


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ImageAndTextBlock.text'
        db.alter_column('fancypages_imageandtextblock', 'text', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'ImageAndTextBlock.text'
        db.alter_column('fancypages_imageandtextblock', 'text', self.gf('django.db.models.fields.CharField')(max_length=2000))

    models = {
        'assets.imageasset': {
            'Meta': {'object_name': 'ImageAsset'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['{}']".format(AUTH_USER_MODEL)}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        AUTH_USER_MODEL: {
            'Meta': {'object_name': AUTH_USER_MODEL_NAME},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fancypages.carouselblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'CarouselBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_1': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_10': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_2': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_3': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_4': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_5': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_6': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_7': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_8': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'image_9': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
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
            'Meta': {'unique_together': "(('name', 'content_type', 'object_id'),)", 'object_name': 'Container'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'fancypages.contentblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'ContentBlock'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blocks'", 'to': "orm['fancypages.Container']"}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fancypages.fancypage': {
            'Meta': {'object_name': 'FancyPage'},
            'date_visible_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_visible_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pages'", 'symmetrical': 'False', 'to': "orm['fancypages.PageGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['fancypages.PageType']"}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'fancypages.fourcolumnlayoutblock': {
            'Meta': {'object_name': 'FourColumnLayoutBlock'},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.horizontalseparatorblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'HorizontalSeparatorBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.imageandtextblock': {
            'Meta': {'object_name': 'ImageAndTextBlock', '_ormbases': ['fancypages.ContentBlock']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'image_text_blocks'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u'Your text goes here.'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.imageblock': {
            'Meta': {'object_name': 'ImageBlock', '_ormbases': ['fancypages.ContentBlock']},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'image_asset': ('fancypages.assets.fields.AssetKey', [], {'blank': 'True', 'related_name': "'image_blocks'", 'null': 'True', 'to': "orm['assets.ImageAsset']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.orderedcontainer': {
            'Meta': {'object_name': 'OrderedContainer', '_ormbases': ['fancypages.Container']},
            'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'fancypages.pagegroup': {
            'Meta': {'object_name': 'PageGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'fancypages.pagenavigationblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'PageNavigationBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'is_relative': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'fancypages.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fancypages.tabblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TabBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.textblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TextBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "'Your text goes here.'"})
        },
        'fancypages.threecolumnlayoutblock': {
            'Meta': {'object_name': 'ThreeColumnLayoutBlock'},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'})
        },
        'fancypages.titletextblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TitleTextBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "'Your text goes here.'"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Your title goes here.'", 'max_length': '100'})
        },
        'fancypages.twitterblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'TwitterBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'max_tweets': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fancypages.twocolumnlayoutblock': {
            'Meta': {'object_name': 'TwoColumnLayoutBlock'},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'left_width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6', 'max_length': '3'})
        },
        'fancypages.videoblock': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'VideoBlock', '_ormbases': ['fancypages.ContentBlock']},
            'contentblock_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fancypages.ContentBlock']", 'unique': 'True', 'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video_code': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['fancypages']
