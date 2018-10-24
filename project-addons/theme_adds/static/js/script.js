$("#contact_us_main_form").each(function(){
    jQuery.validator.setDefaults({
      debug: true,
      success: "valid"
    });
    $( "#contact_us_main_form" ).validate({
      rules: {
        field: {
          required: true,
          email: true
        }
      }
    });
});
/* Category menu toggle open */
$('a.to-toggle-menu').click(function(){
    $(this).next('.custom-menu-inside-div').toggle();
    return false;
});
/* Breadcrumb in category page */
/*$(document).ready(function(){
    var pathname = document.location.pathname;
        search = document.location.search;
    alert('pathname:' +pathname.split('/page')[0]+ '; Tag id:' +new URLSearchParams(search).get('tags'));
});*/
$( ".all-category-div li a" ).each(function() {
    var pathname = document.location.pathname;
        url = pathname.split('/page')[0];
        current= $(this);

    if (current.attr("href") == url ){
        $(".select-nevigation-span").html("/");
        $(".select-nevigation-child").attr("href", url);
        $(".select-nevigation-child").html(current.html());
    }
});
$( ".wp_products_grid_tags a.product-tag" ).each(function() {
    var search = document.location.search;
        url = new URLSearchParams(search).get('tags');
        current= $(this);

    url = '/shop?tags='+url;
    if (current.attr("href") == url ){
        $(".select-nevigation-span").html("/");
        $(".select-nevigation-child").attr("href", url);
        $(".select-nevigation-child").html(current.html());
    }
});