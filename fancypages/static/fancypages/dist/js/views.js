FancypageApp.module('Views', function (Views, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    console.log("Setting up the Views module");

    Views.EditorControls = Backbone.View.extend({
        el: '.fp-editor-controls',
        events: {
            'click #editor-close': 'closeEditor'
        },
        closeEditor: function () {
            console.log("closing editor");
            this.trigger('close-editor');
        }
    });

    Views.EditorHandle = Backbone.View.extend({
        el: '#editor-handle',
        events: {
            'click': 'openPanel'
        },
        openPanel: function () {
            this.trigger('open-panel');
        },
        show: function () {
            console.log("show handle");
            this.$el.trigger('show');
        },
        hide: function () {
            console.log("hide handle");
            this.$el.trigger('hide');
        },
    });

    Views.EditorPanel = Backbone.View.extend({
        el: '#editor-panel',
        initialize: function () {
            _.bindAll(this, 'hide');
            _.bindAll(this, 'show');

            this.controls = new Views.EditorControls();
            this.controls.bind('close-editor', this.hide);

            this.handle = new Views.EditorHandle();
            this.handle.bind('open-panel', this.show);
        },
        show: function () {
            console.log("Show editor panel");
            this.handle.show();
            $('body').removeClass('editor-hidden');
            $.cookie('fpEditorOpened', true);
        },
        hide: function () {
            console.log("Hide editor panel");
            this.handle.hide();
            $('body').addClass('editor-hidden');
            $.cookie('fpEditorOpened', false);
        }
    });

    Views.ContentBlockView = Backbone.View.extend({
        events: {
            'click >.fp-btn.edit-button': 'editBlock',
            'click >.fp-btn.move': 'moveBlock',
            'click >.fp-btn.delete': 'deleteBlock',
            'mouseenter': 'toggleVisibility',
            'mouseleave': 'toggleVisibility'
        },
        toggleVisibility: function () {
            if (!$('body').hasClass('editor-hidden')) {
                this.$el.toggleClass('block-hover');
            } else {
                this.$el.removeClass('block-hover');
            };
        },
        editBlock: function () {
            console.log("edit", this.model.get('id'));
            this.trigger('update-block', 'edit', this.model);
        },
        moveBlock: function () {
            console.log("move", this.model.id);
            this.trigger('update-block', 'move', this.model);
        },
        deleteBlock: function () {
            console.log("delete", this.model.id);
            this.trigger('update-block', 'delete', this.model);
        }
    });

    Views.PageView = Backbone.View.extend({
        el: ".editable-page-wrapper",

        initialize: function () {
            console.log("Initialize page container");

            var self = this;
            this.subviews = [];

            _.bindAll(this, 'updateBlock');

            _.each($('.block', this.$el), function (elem) {
                var block = new FancypageApp.Models.ContentBlock({
                    id: $(elem).data('block-id'),
                    containerId: self.$el.data('container-id')
                });

                var blockView = new Views.ContentBlockView({
                    model: block,
                    el: elem
                });

                blockView.bind('update-block', self.updateBlock);
                self.subviews.push(blockView);
            });
        },
        updateBlock: function (type, block) {
            this.trigger('update-block', type, block);
        }
    });

    Views.EditorFormView = Backbone.View.extend({
        el: '#block-input-wrapper',

        initialize: function () {
            _.bindAll(this, 'render');
            _.bindAll(this, 'updateBlock');

            this.model = new FancypageApp.Models.BlockForm({});
            this.model.on("sync", this.render);

            console.log("init editor form view", this.model);
        },

        updateBlock: function (type, block) {
            this.model.set('id', block.get('id'));
            this.model.fetch();
        },
        render: function () {
            console.log("rendering form view", this.model);
            //this.$el.html(
        }
    });

    var formView = new Views.EditorFormView();

    
});
