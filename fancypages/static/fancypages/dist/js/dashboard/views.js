FancypageApp.module('Dashboard.Views', function (Views, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    var Models = FancypageApp.Dashboard.Models;

    Views.PageNode = Marionette.CompositeView.extend({
        tagName: 'ol',
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
        onCompositeCollectionRendered: function () {
            if (this.model.get('parent') !== null) {
                var treeId = this.model.get('parent') + '-tree';

                this.$el.attr('id', treeId);
                this.$el.addClass('collapse');
            }
        }
    });

    Views.PageTree = Marionette.CollectionView.extend({
        el: 'ol.fp-page-tree',
        itemView: Views.PageNode,
    });
});
