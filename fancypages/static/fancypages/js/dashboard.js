var fancypages = fancypages || {};
fancypages.dashboard = {
    pages: {
        init: function () {
            var pageSortable = $('#pages-sortable');
            pageSortable.nestedSortable({
                forcePlaceholderSize: true,
                opacity: 0.6,
                isTree: true,
                items: 'li.sortable',
                handle: 'div',
                //toleranceElement: '> div',
                placeholder: 'nested-sortable-placeholder',
                start: function (event, ui) {
                    $(this).data('old-position', ui.item.index());
                },
                update: function (event, ui) {
                    var parentPage = $(ui.item).parents('li');
                    var oldIndex = $(this).data('old-position');
                    var newIndex = ui.item.index();

                    var parentId = 0;
                    if (parentPage.length) {
                        parentId = parentPage.data('page-id');
                    }
                    var moveUrl = fancypages.apiBaseUrl + "page/" + $(ui.item).data('page-id') + '/move';
                    $.ajax({
                        url: moveUrl,
                        type: 'PUT',
                        data: {
                            parent: parentId,
                            new_index: newIndex,
                            old_index: oldIndex
                        },
                        beforeSend: function (xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
                        },
                        success: function (data) {
                            window.location.reload();
                        },
                        error: function () {
                            oscar.messages.error(
                                "An error occured moving the page, please try again."
                            );
                        }
                    });
                    $(this).removeAttr('data-old-position');
                }
            });
            $('.tree li:last-child').addClass('last');
        }
    }
};
