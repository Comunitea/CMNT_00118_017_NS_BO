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
            required: 'This field is required',
            email: 'Please enter a valid email address'
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

/* Ajax "Add to cart" */
odoo.define('product_quick_view.quick_view', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var msg_success = 'This product was added to cart';
    //
    // On the shop page
    //
    $('.oe_product_cart form').on('submit', function(event){
        event.preventDefault();

        var msg_div = $(this).find('.add-to-cart-message');
        var prod_id = $(this).find('input[name="product_id"]').val();

        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'product_id': parseInt(prod_id, 10),
            'set_qty': 1
        }).then(function (data) {
            if (data.warning) {
                $(msg_div).html(data.warning);
                $(msg_div).parent().addClass('add-error').slideDown();
            } else {
                $(msg_div).html(msg_success);
                $(msg_div).parent().removeClass('add-error').slideDown();
            }
            // cart quantity change
            $('#header-cart .my_cart_quantity').html(data.cart_quantity);
            // auto close
            setTimeout(function(){
                $(msg_div).parent().slideUp();
            }, 4500);
        });
    });
    //
    // On the product page
    //
    $('.p_ad2cart a#add_to_cart').each(function(){
        $(this).removeAttr('href'); // disable page scroll to top
    });
    $('form.js_add_cart_variants').on('submit', function(event){
        event.preventDefault();

        var msg_div  = $(this).find('.add-to-cart-message');
        var prod_id  = $(this).find('input[name="product_id"]').val();
        var prod_qty = $(this).find('input[name="add_qty"]').val();

        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'product_id': parseInt(prod_id, 10),
            'set_qty': parseInt(prod_qty, 10)
        }).then(function (data) {
            if (data.warning) {
                $(msg_div).html(data.warning);
                $(msg_div).parent().addClass('add-error').slideDown();
            } else {
                $(msg_div).html(msg_success);
                $(msg_div).parent().removeClass('add-error').slideDown();
            }
            // cart quantity change
            $('#header-cart .my_cart_quantity').html(data.cart_quantity);
            // auto close
            setTimeout(function(){
                $(msg_div).parent().slideUp();
            }, 4500);
        });
    });
});
/* Close popup "Was added" message */
$('.wp-close').click(function(){
    $(this).parent().slideUp();
});