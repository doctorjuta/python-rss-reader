function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function load_news() {
    var page_c = parseInt($("#news_block").attr("data-page"));
    var target_page = window.location.protocol+"//"+window.location.host+window.location.pathname+"load/";
    console.log(target_page);
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type:"POST",
        url:target_page,
        data:{requesttype:"infintyupdate",page_c:page_c},
        beforeSend:function(xhr,settings){
            $("#news_block_loading").css('display', 'block');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        error:function(errresp){
            console.log(errresp);
            loading = false;
        },
        success:function(resp){
            $("#news_block_loading").css('display', 'none');
            $("#news_block").append(resp);
            $("#news_block").attr("data-page",page_c+1);
            loading = false;
        }
    });
}
var loading;
$(document).ready(function(){
    if ( $("#news_block").length > 0 ) {
        load_news();
        $(window).scroll(function(){
            if ( loading || $("#news_block_nomore").length > 0 ) { return false; }
            if ( $("#news_block").innerHeight()-($(this).scrollTop()+$(this).height()) <0 ) {
                loading = true;
                load_news();
            }
        });
    }
});