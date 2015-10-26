//
// Create by Konstantyn Davidenko (c)2015
//
//

function getCart()
{
    $jq.ajax({
        type: "GET",
        dataType: 'html',
        url: "/cart/",
        success: function(data){
            $jq('#cart').html(data);
            $jq('#openModal_Cart').show();
            $jq(document.body).addClass("modal"); // При открытии
        }
    });
}

function cartClose(id)
{
    $jq('#'+id).hide();
    $jq(document.body).removeClass("modal"); // При закрытии
}
function isInt(value) {
  if (isNaN(value)) {
    return false;
  }
  var x = parseFloat(value);
  return (x | 0) === x;
}

function toCart (product_id, qty) {
    if (isInt(qty)) {
        if ( qty <= 0 ) {
            qty = 1
        }
    }
    else{
        qty = 1
    }
    $jq.ajax({
        type: "POST",
        url: '/add_to_cart/',
        data: {
            csrfmiddlewaretoken: $jq("input[name=csrfmiddlewaretoken]").val(),
            product_id: product_id,
            qty: qty
        },
        dataType: 'html',
        success: function(data){
            $jq('#cart').html(data);
            $jq('#openModal_Cart').show();
        }
    });
}

function removeFromCart (product_id, url) {
    $jq.ajax({
        type: "POST",
        url: url,
        data: {
            csrfmiddlewaretoken: $jq("input[name=csrfmiddlewaretoken]").val(),
            product_id: product_id
        },
        dataType: 'html',
        success: function(data){
            $jq('#cart').html(data);
            $jq('#openModal_Cart').show();
        }
    });
}
function logIn () {
    $jq.ajax({
        type: "GET",
        url: "/login/",
        dataType: 'html',
        success: function(data){
            $jq('#MyModalData').html(data);
            $jq('#MyModal').show();
        }
    });
}
function views (element_id, button_id ,hide) {
    if (hide){
        jQuery(element_id).slideUp('slow');
        jQuery(button_id).toggleClass("highlight");
    } else {
        jQuery(element_id).slideToggle('slow');
        jQuery(button_id).toggleClass("highlight");
    }
}

function filterApply(page){
    if (isInt(page)){}else{page=1}
    $jq.ajax({
        type: "GET",
        url: '/ajax',
        data: {
            product_on_page: $jq('#product_on_page').val(),
            sort_by: $jq('#sort_by').val(),
            part_id: 1,
            size: [17.0],
            page: page

        },
        dataType: 'html',
        success: function(data){
            $jq('#products').html(data);

        }
    });
}

function addCompare(product_id){
    $jq.ajax({
        type: "GET",
        url: '/add_compare',
        data: {
            product_id: product_id
        },
        dataType: 'html',
        success: function (data) {
            alert('Добавлен')
        }
    });
}
