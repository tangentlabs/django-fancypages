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
        move: function (data) {
            return this.save(data, {
                url: this.url() + '/move'
            });
        },
        url: function () {
            return FancypageApp.Api.baseUrl + '/page/' + this.id;
        }
    });

    Models.Pages = Backbone.Collection.extend({
        model: Models.Page,
        url: FancypageApp.Api.baseUrl + '/pages'
    });
});
