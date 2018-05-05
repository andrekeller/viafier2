function hidemenu() {
    if (window.matchMedia('(max-width: 768px)').matches) {
        $('nav ul li:gt(0)').hide();
    } else {
        showmenu();
    }

}

function showmenu() {
    $('nav ul li:gt(0)').show();
}

$(document).ready(hidemenu);
$(window).resize(hidemenu);

$('nav ul li.nav-title div').click(function() {
    if ($('nav ul li:gt(0)').is(':visible')) {
        hidemenu();
    } else {
        showmenu();
    }
});
