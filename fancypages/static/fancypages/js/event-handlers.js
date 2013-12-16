var fancypages = fancypages || {};

fancypages.eventHandlers = {
    /**
     * Add a new tab to an existing tab block.
     */
    addNewTab: function (ev) {
        ev.preventDefault();

        $.ajax({
            url: $(this).data('action'),
            type: 'POST',
            data: {
                block: $(this).parents('.block').data('block-id')
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
            },
            success: function (data) {
                parent.fancypages.editor.reloadPage();
            },
            error: function () {
                parent.fancypages.utils.messages.error(
                    "An error occured trying to add a new tab. Please try it again."
                );
            }
        });
    },

    deleteTab: function (ev) {
        ev.preventDefault();

        $.ajax({
            url: $(this).data('action'),
            type: 'DELETE',
            data: {
                content_type: $(this).data('content-type-id'),
                object_id: $(this).parents('.block').data('block-id')
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
            },
            success: function (data) {
                parent.fancypages.editor.reloadPage();
            },
            error: function () {
                parent.fancypages.utils.messages.error(
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

        $(this).parents('.fp-asset-input').addClass('editing');
        var fullscreenModal = $("#fullscreen-modal");
        var iframeHtml = "<iframe id='" + iframeId + "' frameborder='0' width='99%' height='360'></iframe>";
        $(".fp-modal-body", fullscreenModal).html(iframeHtml);
        fullscreenModal.modal('show');

        var assetManager = $('#' + iframeId),
            modalHeight = fullscreenModal.height() - 100;
            heading = $(this).data('heading');
        assetManager.attr('src', $(this).data('iframe-src'));
        fullscreenModal.find('.fp-modal-header h3').text(heading);

    },

    /**
     * Open the block selection modal and attach the container ID of the
     * current element to the form to make sure that submitting it to the API
     * has access to the container that tiggered the adding of content.
     */
    showBlockSelection: function (ev) {
        var elem = $(this),
            modalElem = $(elem.data('target')),
            containerId = elem.data('container-id');
        $('button', modalElem).attr('data-container-id', containerId);
        modalElem.modal('show');
    },

    /**
     * Create a new block via the RESTful API. It expects a 'data-container-id'
     * and 'data-block-code' attribute on the triggering element and submits
     * both values as a POST call to the REST API. On success the page is
     * reloaded, otherwise an error message is displayed to the user.
     */
    createNewBlock: function (elem) {
        console.log("CREATING A NEW BLOCK", elem);
        $.ajax({
            url: $(elem).data('api-url'),
            type: 'POST',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
            },
            data: {
                container: $(elem).data('container-id'),
                code: $(elem).data('block-code')
            },
            success: function () {
                fancypages.editor.reloadPage();
            },
            failure: function () {
                fancypages.messages.error(
                    "The new content block could not be created, please try " +
                    "again or contact the site's admin"
                )
            }
        });
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
                var target = $($(elem).data('target')),
                    heading = $(elem).data('heading');
                target.parents('.fp-modal').modal('show').find('.fp-modal-header h3').text(heading);
                target.html(data.rendered_form);

                // prevent collapse events within the modal from closing the modal
                target.find('#pages-sortable [id*="tree"]').on({
                    hide: function (event) {
                        event.stopPropagation();
                    }
                });
            },
            error: function () {
                fancypages.utils.messages.error("Unable to load list of available blocks.");
            }
        });
    },
    /**
     * Delete a content block using the API. The block ID needs to be retrieved
     * from the blocker wrapper <div> which is a parent of the clicked delete
     * button. A page reload is triggered when the block has been deleted successfully.
     */
    deleteBlock: function () {
        var block = $(this).parents('.block');

        $.ajax({
            url: fancypages.apiBaseUrl + 'block/' + $(block).data('block-id'),
            type: 'DELETE',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
            },
            success: function (data) {
                fancypages.editor.reloadPage();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                fancypages.utils.messages.error(
                    "An error occured trying to delete a block. " +
                    "Please try it again."
                );
            }
        });
    },
    /**
     * Load block form when edit button is clicked, add slider if a range
     * value is available for the block and scroll to the right position on
     * the page.
     */
    editWidget: function (ev) {
        var block = $(this).closest('.block');
        fancypages.editor.scrollToWidget(block);

        // Add Class to block editing
        $('.block').removeClass('editing');
        block.addClass('editing');

        fancypages.panels.showEditPanel();

        fancypages.editor.loadBlockForm($(block).data('block-id'), $(block).data('container-name'), {
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
                        var blockId = $(this).parents('form').data('block-id');
                        var previewField = $('#block-' + blockId);
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
     * Display form containing block settings in editor panel.
     */
    displayBlockForm: function (options, data) {
        var blockWrapper = $('div[id=block_input_wrapper]');
        blockWrapper.html(data);
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
