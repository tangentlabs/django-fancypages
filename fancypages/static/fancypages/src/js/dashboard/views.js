FancypageApp.module('Dashboard.Views', function (Views, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    var Models = FancypageApp.Dashboard.Models;

    Views.PageNode = Marionette.CompositeView.extend({
        tagName: 'li',
        itemViewContainer: 'ol',
        template: "#template-page-node",
        events: {
            'hide [id$=-tree]': 'hideChildren',
            'show [id$=-tree]': 'showChildren'
        },
        initialize: function () {
            this.create
            this.collection = this.model.get('children')
        },
        hideChildren: function (ev) {
            var anchor = $('[data-target=#' + this.model.id + '-tree]>i');
            anchor.removeClass('icon-caret-down');
            anchor.addClass('icon-caret-right');
        },
        showChildren: function (ev) {
            var anchor = $('[data-target=#' + this.model.id + '-tree]>i');
            anchor.removeClass('icon-caret-right');
            anchor.addClass('icon-caret-down');
        },
        onCompositeModelRendered: function () {
            this.$el.attr('data-index', this.model.collection.indexOf(this.model));
            this.$el.attr('data-page-id', this.model.id);

            if (this.model.get('parent') !== null) {
                var treeId = this.model.get('parent') + '-tree';

                this.$el.attr('id', treeId);
                this.$el.addClass('collapse');
            }
        },
    });

    Views.PageTree = Marionette.CollectionView.extend({
        el: 'ol.fp-page-tree',
        itemView: Views.PageNode,
        initialize: function () {
            this.sortable = this.$el.sortable({
                placeholder: '<li class="placeholder">Insert here!</li>',
                onDrop: this.saveMovedPage,
            });
        },
        saveMovedPage: function ($item, container, _super, event) {
            _super($item, container);

            var items = container.$getChildren(container.el, "item"),
                newIndex = items.index($item),
                oldIndex = $item.data('index');

            var page = new Models.Page({
                uuid: $item.data('page-id'),
            });
            var promise = page.move({
                parent: $(container.el).data('parent-id'),
                new_index: newIndex,
                old_index: oldIndex,
            });
            promise.complete(FancypageApp.Api.reloadPage);
        }
    });
});
