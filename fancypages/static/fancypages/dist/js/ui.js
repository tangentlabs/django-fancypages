// initialise fitVids plugin for resizing IFRAME YouTube videos
function initFitvids() {
  $('.block-video').fitVids();
}

function initFlexSlider() {
    $('.flexslider').flexslider({
        animation: "slide",
        pauseOnHover: true,
        slideshow: true,
        slideshowSpeed: 2000
    });
}

$(document).ready(function() {
    initFitvids();
    initFlexSlider();
});
