/* Category menu toggle open */
$('a.to-toggle-menu').click(function(){
    $('.custom-menu-inside-div').toggle();
    return false;
});
/* Breadcrumb in category page */
$(document).ready(function(){
    //alert(document.location.pathname + document.location.search);
});
$( ".all-category-div li a" ).each(function() {
    var url = document.location.pathname + document.location.search;
    var current= $(this);
    if (current.attr("href") == url ){
        $(".select-nevigation-span").html("/");
        $(".select-nevigation-child").attr("href", url);
        $(".select-nevigation-child").html(current.html());
    }
});
$( ".wp_products_grid_tags a.product-tag" ).each(function() {
    var url = document.location.pathname + document.location.search;
    var current= $(this);
    if (current.attr("href") == url ){
        $(".select-nevigation-span").html("/");
        $(".select-nevigation-child").attr("href", url);
        $(".select-nevigation-child").html(current.html());
    }
});