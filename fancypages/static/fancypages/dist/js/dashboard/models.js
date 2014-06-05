FancypageApp.module('Dashboard.Models', function (Models, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    Models.Page = Backbone.Model.extend({
        idAttribute: 'uuid',
        defaults: {
            uuid: null,
            name: null,
            url: null,
            status: null,
            isVisible: false,
            children: [],
        },
        initialize: function () {
            this.set('children', new Models.Pages(this.get('children')));
        },
    });

    Models.Pages = Backbone.Collection.extend({
        model: Models.Page,
        url: FancypageApp.Api.baseUrl + '/pages'
    });
});
