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
            required: 'Este campo es requerido',
            email: 'Por favor, introduce una dirección válida'
        }
      }
    });
    // Progressive Web App and SEO. Register Service Worker
    if('serviceWorker' in navigator) {

       if('localhost' !== window.location.hostname){
            navigator.serviceWorker.register('/sw.js').then(function() {
                console.log("Service Worker Registered in: " + window.location.host);
            });
       } else {
            navigator.serviceWorker.getRegistrations().then(function(registrations) {
                if(registrations && registrations.length) {
                    for(let registration of registrations) {
                        registration.unregister()
                    }
                    console.log("Unregister Service Workers in: " + window.location.host);
                }
            });
            console.log("Service Worker Not Registered in: " + window.location.host);
       }
    }
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
    var msg_success = 'Este producto fue agregado al carrito';
    //
    // On the shop page
    //
    $('.oe_product_cart form').on('submit', function(event){
        event.preventDefault();

        var msg_div = $(this).find('.add-to-cart-message');
        var prod_id = $(this).find('input[name="product_id"]').val();
        var spn_div = $(this).find('.oe_product_image');
        var spinner = '<div class="wp-load-spinner"/>';

        $(spn_div).append(spinner);
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'product_id': parseInt(prod_id, 10),
            'add_qty': 1
        }).then(function (data) {
            $(spn_div).find('.wp-load-spinner').fadeOut(300);
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
                $(spn_div).find('.wp-load-spinner').detach();
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
        var spn_div = $(this).find('#product_details');
        var spinner = '<div class="wp-load-spinner spinner-left"/>';

        $(spn_div).append(spinner);
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'product_id': parseInt(prod_id, 10),
            'add_qty': parseInt(prod_qty, 10)
        }).then(function (data) {
            $(spn_div).find('.wp-load-spinner').fadeOut(300);
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
                $(spn_div).find('.wp-load-spinner').detach();
            }, 4500);
        });
    });
    //
    // On the Wishlist page
    //
    $('.go_to_product_wishlist a.add-to-cart').click(function(event){
        event.preventDefault();

        var msg_div = $(this).parents('.wishlist-product-name-div').find('.add-to-cart-message');
        var prod_id = $(this).attr('data-id');
        var spn_div = $(this).parents('.wishlist-product-name-div');
        var spinner = '<div class="wp-load-spinner spinner-sm"/>';

        $(spn_div).append(spinner);
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'product_id': parseInt(prod_id, 10),
            'set_qty': 1
        }).then(function (data) {
            $(spn_div).find('.wp-load-spinner').fadeOut(300);
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
                $(spn_div).find('.wp-load-spinner').detach();
            }, 4500);
        });

    });
});
/* Close popup "Was added" message */
$('.wp-close').click(function(){
    $(this).parent().slideUp();
});
/* Cart onchange recalculation and hiding buttons of control */
$('.oe_website_sale').each(function () {

    var oe_website_sale = this;

    $(oe_website_sale).on("change", "input.js_quantity", function () {
        $('.wp-load-spinner-clear-cart').show();
        setTimeout(function(){
            var sum = 0;
            $('.js_quantity').each(function(){
                if($(this).val()){
                    sum += parseFloat($(this).val());
                }else{
                    sum += 0;
                }
            });
            if(sum){
                //console.log(sum);
            }else{
                $('.clear_shopping_cart').hide();
                $('.cart-main-div-full').hide();
                $('.empty_cart_message').show();
            }
            $('.wp-load-spinner-clear-cart').hide();
        }, 500);
    });
});
/* parts/odoo/addons/website_sale/static/src/js/website_sale.js:171
$('.clear_shopping_cart').hide(); $('.cart-main-div-full').hide(); $('.empty_cart_message').show(); $('.clear_shopping_cart').click(); */

/* Youtube video auto stop on closing (modal product window) */
$(document).ready(function(){
    var stopVideo = function(player) {
        var vidSrc = player.attr('src');
        player.attr('src', '');
        player.attr('src', vidSrc);
    };
    $(document).on('click', '.popup-close', function(){
        stopVideo($('.popup_iframe_url'));
    });
});

/* Variable product change */
$('ul.js_add_cart_variants').each(function(){

    var arr = new Map();
    $('#product_variant_ids_variants_ul li').each(function(){
        var key = $(this).attr('data-id')
            val = $(this).html()
        arr.set(key, val)
    });

    if(arr.size > 0){

        $(document).on('change', 'input[name="product_id"]', function(){
            var key = parseFloat($(this).val());
            var val = parseFloat(arr.get(''+key+''));

            val = val.toFixed(2);
            if($('.price_sin_iva .oe_currency_value')){
                $('.price_sin_iva .oe_currency_value').html(val);
            }
        });

        $(document).on('change', 'input.js_variant_change', function(){
            $('input[name=product_id]').trigger('change');
        });

    }
});

/* Set current tag class */
$('a.product-tag').each(function(){
    var search  = document.location.search
        current = new URLSearchParams(search).get('tags')
        is_search = new URLSearchParams(search).get('search');
        pathname = document.location.pathname;
        url = pathname.split('/page')[0];

    if(current){
        current = '/shop?tags='+current;
    }else if(!(is_search)){
        current = url;
    }

    if ($(this).attr("href") == current ){
        $(this).parents('span').addClass('current');
    }
});

/* Set search breadcrumbs */
$(document).ready(function(){
    var is_search = new URLSearchParams(document.location.search).get('search')
        search_message = 'Resultados de búsqueda';

    if(is_search){
        $(".select-nevigation-span").html("/");
        $(".select-nevigation-child").attr("href", document.location);
        $(".select-nevigation-child").html(search_message);
    }
});

/* Clear wishlist list spinner */
$('a.clear-all-wishlist').click(function(){
    $('.wp-load-spinner-clear-wishlist').show();
});

/* Clear cart spinner */
$('a.clear_shopping_cart').click(function(){
    $('.wp-load-spinner-clear-cart').show();
});

/* Show search bar on mobile header */
/* $('.mobile-search-button').click(function(){
    $('.new_hd_search').toggle();
    $(this).find('i').toggleClass('fa-search').toggleClass('fa-close');
}); */

/* Hacer funcionar la validación de la aceptación de los términos legales en el formulario del oneCheckOut
   para guardar dirección de los usuarios invitados*/
$(document).ready(function(){
    $('input[name="accepted_legal_terms"]').click(function(){
        if($(this).is(":checked")){
            $(this).attr("value", "123");
        } else {
            $(this).attr("value", "");
        }
    });
    $('label[for="accepted_legal_terms"]').on('click', function(){
        $(input[name="accepted_legal_terms"]).attr("value", "123");
    });
});

/* Add Doofinder library */
var doofinder_script ='//cdn.doofinder.com/media/js/doofinder-classic.7.latest.min.js';
//var doofinder_script ='//cdn.doofinder.com/media/js/doofinder-compact.7.latest.min.js';
(function(d,t){var f=d.createElement(t),s=d.getElementsByTagName(t)[0];f.async=1;
  f.src=('https:'==location.protocol?'https:':'http:')+doofinder_script;
  f.setAttribute('charset','utf-8');
  s.parentNode.insertBefore(f,s)}(document,'script')
);
/* Load Doofinder search widget */
var dfClassicLayers = [{
//var dfCompactLayers = [{
    queryInput: '#doofinder_search',
    hashid: '98a4f858627305e834fb8af7a94442c4',
    zone: 'eu1',
    showInMobile: true,
    display: {
        lang: 'es',
        translations: {
            "Results": "Resultados",
            "Search…": "Buscar...",
            "Sorry, no results found.": "Lo sentimos, no hay resultados",
            "View less…": "Ver menos",
            "View more…": "Ver más",
            "Search": "Buscar",
            "CLOSE": "Cerrar",
            "CLEAR": "Limpiar",
            "FILTER": "Filtro",
            "Query Too Large": "Consulta muy larga"
        },
        currency: {
            symbol: '&euro;',
            decimal: ',',
            thousand: '.',
            precision: 2,
            format: '%v%s'
        },
        initialSearch: true,
        header: {
           show: true
        },
        results: {
            initialLayout: 'grid'
        },
        closeOnClick: true,
        closeIfEmpty: true,
    },
//    searchParams: {
//        rpp: 7
//    }
}];

/* Shop sidebar menu */
$(document).ready(function(){
    $('.shop-sidebar-menu .first-level').hover(function(){
        if($(this).find('div.first-level-inner').length){
            $('.products-grid-main').css('opacity', 0.3);
        }else{
            $('.products-grid-main').css('opacity', 1);
        }
    },function(){
        $('.products-grid-main').css('opacity', 1);
    });
});
