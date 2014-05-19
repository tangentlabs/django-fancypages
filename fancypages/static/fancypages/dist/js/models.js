FancypageApp.module('Models', function (Models, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    Models.Container = Backbone.Model.extend({});
    Models.Containers = Backbone.Collection.extend({
        model: Models.Container
    });

    Models.ContentBlock = Backbone.Model.extend({});
    Models.ContentBlocks = Backbone.Collection.extend({
        model: Models.ContentBlock
    });

    Models.BlockForm = Backbone.Model.extend({
        url: function () {
            console.log("block form for", this.get('id'));
            //var url = FancypageApp.Api.baseUrl + "/block" + this.get('id'), "/form";
            //console.log("URL", url);
            return FancypageApp.Api.baseUrl + "/block/" + this.get('id') + "/form";
        }
    });

});
