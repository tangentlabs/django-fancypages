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

            anchor.removeClass('fp-icon-square-minus');
            anchor.addClass('fp-icon-square-plus');
        },
        showChildren: function (ev) {
            var treeId = $(ev.currentTarget).attr('id'),
                anchor = $('[data-target=#' + treeId + ']>i');

            anchor.removeClass('fp-icon-square-plus');
            anchor.addClass('fp-icon-square-minus');
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
            "show.bs.collapse .row-actions-position .collapse": "pageSelect",
            "shown.bs.collapse .row-actions-position .collapse": "closeActions",
            "click .fp-children-toggle": "toggleChildren"
        },
        initialize: function () {
            this.sortable = this.$el.sortable({
                onDrop: this.saveMovedPage,
                handle: '.fp-pagemove',
            });

            // Set height of sortable container
            $(window).resize(function() {
                $('.fp-page-management').height($(window).height() - 220);
            });
            $(window).trigger('resize');
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

        // Toggle the collapse on child
        toggleChildren: function(ev) {
            ev.stopPropagation();
            var openTarget = $(ev.target).attr('data-target');
            $(openTarget).collapse('toggle');
        },
        
        // Close other page actions
        pageSelect: function(ev) {
            $('.row-actions-position .collapse').not($(ev.target)).each(function(){
                if ($(this).hasClass('in')) {
                    $(this).parent().next().addClass('collapsed');
                }
            });
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
