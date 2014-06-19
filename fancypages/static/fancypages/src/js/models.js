FancypageApp.module('Models', function (Models, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    var oldSync = Backbone.sync;
    Backbone.sync = function(method, model, options){
        options.beforeSend = function(xhr){
            $.cookie('csrfToken');
            xhr.setRequestHeader('X-CSRFToken', FancypageApp.Api.getCsrfToken());
        };
        return oldSync(method, model, options);
    };

    Models.Container = Backbone.Model.extend({
        idAttribute: 'uuid',
    });
    Models.Containers = Backbone.Collection.extend({
        model: Models.Container
    });

    Models.ContentBlock = Backbone.Model.extend({
        idAttribute: 'uuid',
        url: function () {
            return FancypageApp.Api.baseUrl + '/block/' + this.id;
        },
        move: function () {
            return this.save({}, {
                url: this.url() + '/move'
            });
        }
    });
    Models.ContentBlocks = Backbone.Collection.extend({
        model: Models.ContentBlock
    });

    Models.BlockForm = Backbone.Model.extend({
        idAttribute: 'uuid',
        defaults: {
            'container': null,
        },
        url: function () {
            return FancypageApp.Api.baseUrl + "/block/" + this.id + "/form";
        }
    });

    Models.AssetInputModel = Backbone.Model.extend({
        defaults: {
            id: null,
            image: null,
            type: null
        }
    });

    Models.OrderedContainer = Backbone.Model.extend({
        idAttribute: 'uuid',
        url: function () {
            return FancypageApp.Api.baseUrl + "/ordered-container/" + this.id;
        }
    });
    Models.OrderedContainers = Backbone.Collection.extend({
        model: Models.OrderedContainer,
        url: FancypageApp.Api.baseUrl + '/ordered-containers'
    });


    Models.PageLinkForm = Backbone.Model.extend({
        defaults: {
            fieldId: null,
        },
        url: function () {
            return FancypageApp.Api.baseUrl + '/pages/select-form?field_id=' + this.get('fieldId');
        }
    });
});
