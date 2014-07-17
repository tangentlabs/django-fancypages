"use strict"

var FancypageApp = new Marionette.Application();

FancypageApp.on('initialize:after', function () {
    var editorPanel = new FancypageApp.Views.EditorPanel();
    var formView = new FancypageApp.Views.EditorFormView();
    var pageView = new FancypageApp.Views.PageView();

    pageView.bind('update-block', formView.updateBlock);
});
