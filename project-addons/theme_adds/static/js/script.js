$(document).ready(function(){
    $( "#contact_us_main_form" ).validate({
      rules: {
        email_from: {
          required: true,
          email: true
        }
      },
      messages: {
        email_from: {
            required: "Este campo es obligatorio",
            email: "Por favor, introduce una dirección de correo electrónico válida"
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