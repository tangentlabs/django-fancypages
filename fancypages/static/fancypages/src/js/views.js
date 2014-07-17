FancypageApp.module('Views', function (Views, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    /**
     * Rich text editor view that provides integration with the Froala editor.
     */
    Views.FroalaEditor = Marionette.View.extend({
        editorOptions: {
            inlineMode: false,
            buttons: ['bold', 'italic', "createLink", "insertOrderedList", "insertUnorderedList", "html"],
        },
        initialize: function (options) {
            _.bindAll(this, 'updatePreview');

            var self = this,
                defaults = {
                    contentChangedCallback: this.updatePreview
                };

            this.block = options.block;
            this.textarea = $('textarea', this.$el);

            _.extend(defaults, this.editorOptions);
            this.textarea.editable(defaults);

            this.editor = $('.froala-element', this.$el);
        },
        updatePreview: function (ev) {
            var fieldName = $(this.textarea).attr('id').replace('id_', ''),
                previewField = $('#block-' + this.block.id + '-' + fieldName);

            $(previewField).html(this.editor.html());
        }
    });

    /**
     * Rich text editor view that provides integration with the Trumbowyg
     * editor.
     */
    Views.TrumbowygEditor = Marionette.View.extend({
        editorOptions: {
            fullscreenable: false,
            closable: false,
            btns: ['bold', 'italic',
                '|', 'link', '|', 'unorderedList', 'orderedList',
                '|', 'viewHTML']
        },
        initialize: function (options) {
            var self = this; 

            _.bindAll(this, 'updatePreview');

            this.block = options.block;
            this.textarea = $('textarea', this.$el);

            this.textarea.trumbowyg(this.editorOptions);
            this.editor = $('.trumbowyg-editor', this.$el);

            this.editor.on('change', this.updatePreview);
            this.editor.on('keyup', this.updatePreview);
            $('button', this.$el).on('click', this.updatePreview);
        },
        updatePreview: function (ev) {
            var fieldName = $(this.textarea).attr('id').replace('id_', ''),
                previewField = $('#block-' + this.block.id + '-' + fieldName);

            $(previewField).html(this.textarea.val());
        }
    });

    /**
     * Initialize the view module with options passed in from the main
     * app. Options handled by the initializer are:
     *
     * editor: 
     * editorView: A backbone/marionette view object that implements the rich text
     *      editor. This view will be initialised for every from element that
     *      is wrapped in 'div.rte-wrapper'. The view needs to handle the
     *      preview updating of the editor within the view to work correctly.
     */
    Views.addInitializer(function (options) {
        options = options || {};
        switch (options.editor || 'trumbowyg') {
            case 'custom':
                Views.RichTextEditor = options.editorView;
                break;
            case 'froala':
                Views.RichTextEditor = Views.FroalaEditor;
                break;
            default:
            case 'trumbowyg':
                Views.RichTextEditor = Views.TrumbowygEditor;
                break;
        };

        if (!_.isEmpty(options.editorOptions)) {
            Views.RichTextEditor.editorOptions = options.editorOptions;
        };
    });

    Views.EditorControls = Backbone.View.extend({
        el: '.fp-editor-controls',
        events: {
            'click #editor-close': 'closeEditor'
        },
        closeEditor: function () {
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
            this.$el.trigger('show');
        },
        hide: function () {
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

            if ($.cookie('fpEditorOpened') === 'true') {
                this.show();
            }
        },
        show: function () {
            this.handle.show();
            $('body').removeClass('editor-hidden');
            $.cookie('fpEditorOpened', true);
        },
        hide: function () {
            this.handle.hide();
            $('body').addClass('editor-hidden');
            $.cookie('fpEditorOpened', false);
        }
    });

    Views.ContentBlockView = Backbone.View.extend({
        events: {
            'click >.fp-btn.edit-button': 'editBlock',
            'click >.block-move-delete>.fp-btn.move': 'moveBlock',
            'click >.block-move-delete>.fp-btn.delete': 'deleteBlock',
            'mouseenter': 'showButtons',
            'mouseleave': 'hideButtons'
        },
        initialize: function () {
            var self = this;
            _.each($('>div.fp-tabbable', this.$el), function (elem) {
                new Views.TabbedBlock({el: elem, model: self.model});
            });
        },
        showButtons: function () {
            this.$el.addClass('block-hover');
        },
        hideButtons: function () {
            this.$el.removeClass('block-hover');
        },
        editBlock: function () {
            this.trigger('update-block', 'edit', this.model);
        },
        moveBlock: function () {
            this.trigger('update-block', 'move', this.model);
        },
        deleteBlock: function () {
            this.trigger('update-block', 'delete', this.model);
        }
    });

    Views.PageView = Backbone.View.extend({
        el: ".editable-page-wrapper",

        initialize: function () {

            var self = this;

            _.bindAll(this, 'updateBlock');

            this.initializeVideo();
            this.initializeSlideShow();

            this.sortables = $('.sortable').sortable({
                containerSelector: '.sortable',
                group: 'sortable-containers',
                nested: false,
                handle: '.move',
                itemSelector: '.block',
                placeholder: '<div class="placeholder">Insert here!</div>',
                onDragStart: this.displayMoveGrid,
                onDrop: this.saveMovedBlock,
            });

            _.each($('.block', this.$el), function (elem) {
                var block = new FancypageApp.Models.ContentBlock({
                    uuid: $(elem).data('block-id'),
                    //TODO we need to fix the fact that the ID is supposed to be UUID
                    // and backbone makes some assumptions based on IDs
                    container: $(elem).data('container-id'),
                    languageCode: $(elem).attr('lang')
                });

                var blockView = new Views.ContentBlockView({
                    model: block,
                    el: elem
                });

                blockView.bind('update-block', self.updateBlock);
            });

            var modalView = new Views.BlockTypeView();

            _.each($('.block-add-control', this.$el), function (elem) {
                var view = new Views.BlockSelectionView({el: elem});
                view.bind('open-selection', modalView.showSelection);
            });
        },
        initializeVideo: function () {
            $('.block-video').fitVids();
        },
        initializeSlideShow: function () {
            $('.flexslider').flexslider({
                animation: "slide",
                pauseOnHover: true,
                slideshow: true,
                slideshowSpeed: 2000
            });
        },
        updateBlock: function (type, block) {
            this.trigger('update-block', type, block);
        },
        displayMoveGrid: function ($item, container, _super, event) {
            _super($item, container);
            $('body').addClass('block-move');
        },
        saveMovedBlock: function ($item, container, _super, event) {
            _super($item, container);

            $('body').removeClass('block-move');

            var items = container.$getChildren(container.el, "item"),
                index = items.index($item),
                block = new FancypageApp.Models.ContentBlock({
                    uuid: $item.data('block-id'),
                    container: container.el.data('container-id'),
                    index: index
                });

            var promise = block.move();
            promise.complete(FancypageApp.Api.reloadPage);
        }
    });

    Views.EditorFormView = Backbone.View.extend({
        el: '#block-input-wrapper',
        events: {
            'submit': 'submitForm',
            'change div[data-behaviours~=field-live-update] input': 'updateTextElement',
            'keyup div[data-behaviours~=field-live-update] input': 'updateTextElement'
        },
        /**
         * Initialize view the a BlockForm model that can be used to retrieve
         * the correct form data from the backend API. Receiving updated data
         * for the model results in re-rendering the view.
         */
        initialize: function () {
            _.bindAll(this, 'render');
            _.bindAll(this, 'updateBlock');
            _.bindAll(this, 'initSliders');
            _.bindAll(this, 'initRichTextEditor');
            _.bindAll(this, 'initLinkSelector');

            this.model = new FancypageApp.Models.BlockForm({});
            this.model.on("sync", this.render);

            this.iframeModal = new Views.FullscreenModal();
        },
        /**
         * 
         */
        updateBlock: function (type, block) {
            this.model.set('uuid', block.id);

            switch (type) {
                case 'edit':
                    this.editBlock(block);
                    break;
                case 'move':
                    this.moveBlock(block);
                    break;
                case 'delete':
                    this.deleteBlock(block);
                    break;
                default:
                    break;
            };
        },
        editBlock: function (block) {
            this.model.fetch();
        },
        moveBlock: function (block) {
        },
        deleteBlock: function (block) {
            block.destroy({
                'success': function () {
                    FancypageApp.Api.reloadPage();
                }
            });
        },
        submitForm: function (ev) {
            ev.preventDefault();

            var form = $('form', this.$el),
                submitButton = $('button[type=submit]', this.$el),
                block = new FancypageApp.Models.ContentBlock({});

            if (form.data('locked')) {
                return false;
            } else {
                submitButton.attr('disabled', true);
                form.data('locked', true);
            }
            
            _.each(form.serializeArray(), function (obj) {
                block.set(obj.name, obj.value);
            });

            block.set('code', submitButton.val());
            block.set('container', form.data('container-id'));
            block.set('uuid', form.data('block-id'));


            block.save({}, {type: 'PUT'}).complete(function () {
                submitButton.attr('disabled', false);
                form.data('locked', false);
            }).error(function () {
                this.trigger("error", "An error occured trying to delete a block. Please try it again.");
            }).success(function () {
                FancypageApp.Api.reloadPage();
            });
        },

        /**
         * Update a text block element that has been modified as input/textarea
         * field in a form. The wrapper ID for the corresponding element in the
         * content block is determined based on updated input field and the
         * value of the form field set as the inner-HTML of that block element.
         */
        updateTextElement: function (ev) {
            if (!_.isEmpty(ev)) {
                ev.preventDefault();
            }

            var fieldElem = $(ev.target),
                fieldName = null,
                previewField = null;

            if (!fieldElem || _.isEmpty(fieldElem.attr('id'))) {
                return false;
            }

            fieldName = fieldElem.attr('id').replace('id_', '');
            previewField = $('#block-' + this.model.id + '-' + fieldName);
            previewField.html(fieldElem.val());
        },
        /**
         * Display the form HTML received from the API.
         */
        render: function () {
            var self = this;
            this.$el.html(this.model.get('form'));

            this.initSliders();
            this.initRichTextEditor();
            this.initLinkSelector();

            $('.fp-scroll-content').jScrollPane();

            _.each($('.fp-asset-input', this.$el), function (elem) { 
                var model = new FancypageApp.Models.AssetInputModel({
                    id: $('[name=image_asset]', elem).val(),
                    type: $('[name=image_asset_type]', elem).val(),
                    image: $('img', elem).attr('src')
                });

                var view = new Views.AssetInputView({
                    el: elem,
                    model: model
                });
                view.bind('select-image-clicked', self.iframeModal.showModal);
                self.iframeModal.bind('image-asset-updated', view.setSelectedAsset);
            });
        },
        initSliders: function () {
            var self = this;

            _.each($('[type=range]'), function (elem) {
                var slider = new Views.Slider({
                    el: elem,
                    block: self.model
                });
                slider.render();
            });
        },
        initRichTextEditor: function () {
            var self = this;

            _.each($('.rte-wrapper', this.$el), function (elem) {
                new Views.RichTextEditor({el: elem, block: self.model});
            });
        },
        initLinkSelector: function () {
            _.each($('[data-behaviours=load-link-selector]', this.$el), function (elem) {
                new Views.LinkSelector({el: elem});
            });
        }
    });

    Views.BlockSelectionView = Marionette.View.extend({
        events: {
            'click': 'openBlockSelection'
        },
        openBlockSelection: function () {
            this.trigger('open-selection', $('a', this.$el).data('container-id'));
        }
    });

    Views.BlockTypeView = Marionette.View.extend({
        el: '#block_selection_modal',
        events: {
            'click button': 'createBlock'
        },
        initialize: function () {
            _.bindAll(this, 'showSelection');
        },
        createBlock: function (ev) {
            var button = $(ev.target).closest('button'),
                self = this;

            var model = new FancypageApp.Models.ContentBlock({
                code: button.data('block-code'),
                container: this.containerId
            });

            var promise = model.save({}, {url: button.data('api-url')});
            promise.complete(function () {
                self.$el.modal('hide');
                FancypageApp.Api.reloadPage();
            });
        },
        showSelection: function (container) {
            this.containerId = container;
            this.$el.modal('show');
        }
    });

    Views.AssetInputView = Marionette.View.extend({
        events: {
            'click a': 'selectAsset'
        },
        initialize: function () {
            _.bindAll(this, 'selectAsset');
            _.bindAll(this, 'setSelectedAsset');

            this.modal = null;
        },
        selectAsset: function () {
            var button = $('a', this.$el);
            this.$el.addClass('editing');
            this.origin = button.data('input-name');

            this.trigger(
              'select-image-clicked',
              button.data('heading'),
              button.data('iframe-src'),
              this.origin
            );
        },
        setSelectedAsset: function (type, id, url, origin) {
            this.$el.removeClass('editing');

            if (origin !== this.origin) {
              return false;
            }

            $("input[name=" + this.origin + "]", this.$el).attr('value', id);
            $("input[name=" + this.origin + "_type]", this.$el).attr('value', type);
            $("img", this.$el).attr('src', url);
        }
    });

    Views.Slider = Marionette.View.extend({
        initialize: function (options) {
            _.bindAll(this, 'updateLayout');

            this.block = options.block;
            this.min = parseInt(this.$el.attr('min'));
            this.max = parseInt(this.$el.attr('max'));
        },
        render: function () {
            this.$el.rangeslider({
                polyfill: false,
                onSlide: this.updateLayout
            });
        },
        updateLayout: function (position, value) {
            var blockElem = $('#block-' + this.block.id),
                leftColumn = $('.column-left', blockElem),
                rightColumn = $('.column-right', blockElem);

            if (_.isEmpty(leftColumn) || _.isEmpty(rightColumn)) {
                return false;
            }

            leftColumn[0].className = leftColumn[0].className.replace(/span\d+/g, '');
            leftColumn.addClass('span' + value);

            rightColumn[0].className = rightColumn[0].className.replace(/span\d+/g, '');
            rightColumn.addClass('span' + (this.max - value));
        }
    });

    Views.FullscreenModal = Marionette.View.extend({
        el: '#fullscreen-modal',
        initialize: function (options) {
            _.bindAll(this, 'showModal');
            _.bindAll(this, 'hideModal');
            _.bindAll(this, 'triggerAssetUpdatedEvent');

            this.origin = null;
            this.$iframe = null;
            this.template = _.template($('#fullscreen-modal-template').html() || '');
            this.iframeTemplate = _.template("<iframe frameborder='0' width='99%' height='360'></iframe>");

            this.on("image-asset-updated", this.hideModal);
        },
        showModal: function (heading, url, inputId) {
            var self = this;

            this.origin = inputId;

            this.$el.html(this.template({
                heading: heading,
                bodyHtml: this.iframeTemplate()
            }));

            this.$el.modal('show');

            this.iframe = $('iframe', this.el$);
            this.iframe.attr('src', url);

            // FIXME: we need to clean this up after asset management is move out
            // of the really messy iframe.
            this.iframe.load(function () {
                self.iframe.contents().on(
                    'click',
                    "[data-behaviours~=selectable-asset]",
                    self.triggerAssetUpdatedEvent
                );
            });
        },
        hideModal: function () {
            this.iframe = null;
            this.$el.modal('hide');
        },
        triggerAssetUpdatedEvent: function (ev) {
            ev.preventDefault();

            var target = $(ev.currentTarget),
                type = target.data('asset-type'),
                id = target.data('asset-id'),
                url = $('img', target).attr('src');

            this.trigger("image-asset-updated", type, id, url, this.origin);
            this.origin = null;
        }
    });

    Views.TabbedBlock = Marionette.View.extend({
        events: {
            'click a.fp-add-tab': 'addTab',
            'click i.fp-delete-tab': 'deleteTab'
        },
        initialize: function () {
            _.bindAll(this, 'addTab');

            this.collection = new FancypageApp.Models.OrderedContainers();
            this.collection.bind('sync', FancypageApp.Api.reloadPage);
        },
        addTab: function (ev) {
            this.collection.create({
                block: this.model.id,
                language_code: this.model.get('languageCode')
            }, {url: this.collection.url});
        },
        deleteTab: function (ev) {
            ev.preventDefault();
            var model = new FancypageApp.Models.OrderedContainer({
                uuid: $(ev.target).data('block-id')
            });
            model.destroy().success(FancypageApp.Api.reloadPage);
        }
    });

    Views.LinkSelector = Marionette.View.extend({
        events: {
            'click': 'loadLinks'
        },
        initialize: function () {
            _.bindAll(this, 'loadLinks');
            _.bindAll(this, 'setValue');
            _.bindAll(this, 'render');

            this.heading = this.$el.data('heading');
            this.template = _.template($('#fullscreen-modal-template').html() || '');

            this.model = new FancypageApp.Models.PageLinkForm({
                fieldId: this.$el.data('field-id')
            });
            this.model.bind('sync', this.render);
        },
        loadLinks: function () {
            this.model.fetch();
        },
        setValue: function (ev) {
            ev.preventDefault();
            this.$el.siblings('input').val($(ev.target).attr('href'));
        },
        render: function () {
            var elem = $('#fullscreen-modal'),
                self = this;

            elem.html(this.template({
                heading: this.heading,
                bodyHtml: this.model.get('rendered_form')
            })).modal('show');

            $('a', elem).bind('click', this.setValue);
        }
    });

    var formView = new Views.EditorFormView();
});
