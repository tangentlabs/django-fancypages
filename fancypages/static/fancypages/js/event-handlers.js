var fancypages = fancypages || {};

fancypages.eventHandlers = {
    /**
     * Add a new tab to an existing tab widget.
     */
    addNewTab: function (ev) {
        ev.preventDefault();

        $.ajax({
            url: $(this).data('action'),
            type: 'POST',
            data: {
                content_type: $(this).data('content-type-id'),
                object_id: $(this).parents('.widget').data('widget-id')
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
            },
            success: function (data) {
                parent.fancypages.editor.reloadPreview();
            },
            error: function () {
                parent.oscar.messages.error(
                    "An error occured trying to add a new tab. Please try it again."
                );
            }
        });
    },

    loadIframeModal: function (ev) {
        var iframeId = $(this).data('iframe-id');
        if (iframeId === undefined) {
            return;
        }

        $(this).parents('.asset-input').addClass('editing');
        var fullscreenModal = $("#fullscreen-modal");
        var iframeHtml = "<iframe id='" + iframeId + "' frameborder='0' width='100%' height='100%'></iframe>";
        $(".modal-body", fullscreenModal).html(iframeHtml);
        fullscreenModal.modal('show');

        var assetManager = $('#' + iframeId),
            modalHeight = fullscreenModal.height() - 100;
        assetManager.attr('src', $(this).data('iframe-src'));

        // Set height of the Asset IFrame
        assetManager.attr('height', modalHeight);
    },

    /**
     * Load and display the content of a modal.
     */
    loadModal: function (ev) {
        var elem = this;
        $.ajax({
            url: $(elem).data('href'),
            type: 'GET',
            data: {
                container: $(elem).data('container-id')
            },
            success: function (data) {
                var target = $($(elem).data('target'));
                target.parents('.modal').modal('show');
                target.html(data.rendered_form);
                
                // prevent collapse events within the modal from closing the modal
                target.find('#pages-sortable [id*="tree"]').on({
                    hide: function (event) {
                        event.stopPropagation();
                    }
                });
            },
            error: function () {
                oscar.messages.error("Unable to load list of available widgets.");
            }
        });
    },
    /**
     * Delete a widget
     */
    deleteWidget: function (ev) {
        var widget = $(this).parents('.widget');
        var deleteUrl = '/dashboard/fancypages/widget/delete/' + $(widget).data('widget-id') + "/";

        $.ajax(deleteUrl)
            .done(function (data) {
                var widgetWrapper = $('div[id=widget_input_wrapper]');
                widgetWrapper.after(data);

                $(data).load(function () {
                    $(this).modal('show');
                });
            })
            .error(function () {
                oscar.messages.error(
                    "An error occured trying to delete a widget. Please try it again."
                );
            });
    },
    /**
     * Load widget form when edit button is clicked, add slider if a range
     * value is available for the widget and scroll to the right position on
     * the page.
     */
    editWidget: function (ev) {
        var widget = $(this).closest('.widget');
        fancypages.editor.scrollToWidget(widget);

        // Add Class to widget editing
        $('.widget').removeClass('editing');
        widget.addClass('editing');

        fancypages.panels.showEditPanel();

        fancypages.editor.loadWidgetForm($(widget).data('widget-id'), $(widget).data('container-name'), {
            success: function () {
                // attach slider to column width slider
                var sliderSelection = $('#id_left_width');
                sliderSelection.after('<div id="left-width-slider"></div>');
                sliderSelection.css('display', 'none');
                var slider = $('#left-width-slider');

                var maxValue = sliderSelection.data('max');
                var minValue = sliderSelection.data('min');

                slider.slider({
                    range: "min",
                    value: sliderSelection.val(),
                    min: minValue,
                    max: (maxValue - 1),
                    slide: function (ev, ui) {
                        var widgetId = $(this).parents('form').data('widget-id');
                        var previewField = $('#widget-' + widgetId);
                        var leftColumn = $('.column-left', previewField);

                        leftColumn[0].className = leftColumn[0].className.replace(/span\d+/g, '');
                        leftColumn.addClass('span' + ui.value);

                        var rightColumn = $('.column-right', previewField);
                        rightColumn[0].className = rightColumn[0].className.replace(/span\d+/g, '');
                        rightColumn.addClass('span' + (maxValue - ui.value));

                        sliderSelection.attr('value', ui.value);
                    }
                });
            }
        });
    },
    /**
     * Display form containing widget settings in editor panel.
     */
    displayWidgetForm: function (options, data) {
        var widgetWrapper = $('div[id=widget_input_wrapper]');
        widgetWrapper.html(data.rendered_form);
        $('#page-settings').hide();

        fancypages.editor.wysiwyg.init();
        
        //Init the Select2 plugin for selects in the editor
        $('#editor-panel select').css('width', '100%');
        $('#editor-panel select').select2();
        
        $('.editor').animate({backgroundColor: "#555"}, 500)
                    .delay(500)
                    .animate({backgroundColor: "#444"}, 500);

        fancypages.editor.updateSize();

        if (options && 'success' in options) {
            options.success();
        }
        return false;
    }
};
