// Load more button
$(document).ready(function(){
  window.onscroll = function() {scrollFunction(), loadMore()};
});

function isScrolledIntoView(elem){
  let docViewTop = $(window).scrollTop();
  let docViewBottom = docViewTop + window.innerHeight;

  let elemTop = $(elem).offset().top;
  let elemBottom = elemTop + $(elem).height();
  return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

function loadMore(){
  let switchButton = $('button.active').attr('id');
  if(isScrolledIntoView('.last-item')){
    $('.last-item').removeClass('last-item');
    $('.list-article').append('<div class="col-xs-12 article-wrapper last-item"><article><div class="img-wrapper"><img src="http://lorempixel.com/150/150/abstract" alt="" /></div><h1>Atque quo maxime. <span class="sumary">sumary</span></h1></article></div>');
  }
}


function scrollFunction() {
  if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 20) {
    document.getElementById("top-button").style.display = "block";
  } else {
    document.getElementById("top-button").style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

//Header
$(function(){
  $(window).scroll(function(){
    var winTop = $(window).scrollTop();
    if(winTop >= 30){
      $("body").addClass("sticky-header");
    }else{
      $("body").removeClass("sticky-header");
    }//if-else
  });//win func.
});//ready func.

//Filter
$(".filter-search").keyup(function (e) {
  $(".list-selectors .description").hide();
  $(".list-selectors .description").each(function (e) {
    let founded = $(this).text().toLowerCase();
    let inputVal = $(".filter-search").val().toLowerCase();
    if (founded.indexOf(inputVal) >= 0) {
      $(this).show();
    }
  });
});

$(document).ready(function(){

  $('.description').click(function(){
    if($(this).parent().attr('class') == 'list-selectors'){
      $(this).appendTo($('.filter-selected'))
    } else {
      $(this).appendTo($('.filter-tags .list-selectors'))
    }
    
  });
});
