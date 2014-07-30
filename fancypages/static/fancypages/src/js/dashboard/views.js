FancypageApp.module('Dashboard.Views', function (Views, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    var Models = FancypageApp.Dashboard.Models;

    Views.PageNode = Marionette.CompositeView.extend({
        tagName: 'li',
        itemViewContainer: 'ol',
        template: "#template-page-node",
        events: {
            'show [id$=-tree]': 'showChildren'
        },
        initialize: function () {
            this.collection = this.model.get('children')
            // add this event here to ensure that only this model's hide is
            // triggering this views hideChildren.
            this.events['hidden [id=' + this.model.id + '-tree]'] = 'hideChildren';
        },
        hideChildren: function (ev) {
            var treeId = $(ev.currentTarget).attr('id'),
                anchor = $('[data-target=#' + treeId + ']>i');

            if ($(ev.currentTarget).hasClass('in')) {
                return false;
            }

            anchor.removeClass('icon-caret-down');
            anchor.addClass('icon-caret-right');
        },
        showChildren: function (ev) {
            var treeId = $(ev.currentTarget).attr('id'),
                anchor = $('[data-target=#' + treeId + ']>i');

            anchor.removeClass('icon-caret-right');
            anchor.addClass('icon-caret-down');
        },
        /**
         * After we've rendered the new list element representing a page node,
         * we add the index and page ID to the list node as data attributes.
         */
        onCompositeModelRendered: function () {
            this.$el.attr('data-index', this.model.collection.indexOf(this.model));
            this.$el.attr('data-page-id', this.model.id);

            // set this nodes UUID as the tree ID for the sub-tree and collapse
            // it by default. Nothing is done no sub-tree is present.
            this.$el.children('ol').attr('id', this.model.id + '-tree');
        },
    });

    Views.PageTree = Marionette.CollectionView.extend({
        el: 'ol.fp-page-management',
        itemView: Views.PageNode,
        events: {
            "shown.bs.collapse .row-actions-position .collapse": "closeActions",
        },
        initialize: function () {
            this.sortable = this.$el.sortable({
                placeholder: '<li class="fp-management-placeholder">Insert here!</li>',
                onDrop: this.saveMovedPage,
                handle: 'i.icon-move',
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
        },
        // Close other page actions
        closeActions: function(ev) {
            $('.row-actions-position .collapse').not($(ev.target)).each(function(){
                if ($(this).hasClass('in')) {
                    $(this).collapse('hide');
                }
            });
        }
    });
});
