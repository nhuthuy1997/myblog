// Load more button
$(document).ready(function(){
  window.onscroll = function() {scrollFunction(), loadMore()};

  $('article').last().addClass('last-item');
  clip_post();
  $('.clipjs').removeClass('clipjs');

  $('#loading-img').fadeOut();
  $('.loading-post').fadeOut();
});

function isScrolledIntoView(elem){
  let docViewTop = $(window).scrollTop();
  let docViewBottom = docViewTop + window.innerHeight;
  let elemTop = $(elem).offset().top;
  return ((elemTop <= docViewBottom) && (elemTop >= docViewTop));
}

async function loadMore(){
  if(isScrolledIntoView('.last-item')){
    current_articles = $('article').length
    old_articles = $('.last_request').attr('value');
    if(current_articles == old_articles) {
      await $('.loading-post').fadeToggle();
      await $('.last_request').attr('value', parseInt(old_articles)+10);
      await $.ajax({
        url: window.location.href.concat('/pagination/').concat(current_articles)
      }).done(function(data) {
        $('.last-item').removeClass('last-item');
        $('.list-article .article-wrapper').append(data);
        $('article').last().addClass('last-item');
        clip_post();
        $('.clipjs').removeClass('clipjs');
      });
      await $('.loading-post').fadeToggle();
    }
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

  $(".filter-search").keyup(function(e) {
    if($('.filter-search-flag').val()=='0'){
      $('.filter-search-flag').val('1');
      filter($(this));
    }
  });

  $('.filter-submit').click(function() {
    let hash_tags = [];
    let source_ids = [];
    $('.filter-selected input[type=hidden]').each(function() {
      hash_tags.push($(this).val())
    });
    
    let valid = 0;
    $('input:checked').each(function() {
      source_ids.push($(this).val());
      valid++;
    });
    if(valid){
      let url = window.location.origin.concat('/filter/').concat(hash_tags.join('-')).concat('/').concat(source_ids.join('-'));
      window.location.href = url;
    } else {
      toastr["warning"]("Select at least 1 source. Please!!!")
    }
  });
});//ready func.

//filter
async function filter(ele){
  $('#loading-img').fadeToggle(500);
  await sleep(1000);
  if(!ele.val()){
    $(".list-selectors .result").empty();
    $(".list-selectors .description").show();
    $('.filter-search-flag').val('0');
  } else {
    $(".list-selectors .description").hide();
    $(".list-selectors .result").empty();
    $.ajax({
      url: window.location.origin.concat('/filter/') + ele.val(),
    }).done(function(data){
      $('.filter-tags .result').append(data);
      $('.result .description').click(function(){
        change_tag($(this));
      });
      
    }).always(function() {
      $('.filter-search-flag').val('0');
    });
  }
  $('#loading-img').fadeToggle(500);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

$(document).ready(function(){
  $('.description').click(function(){
    change_tag($(this));
  });
});

function change_tag(ele){
  let value = ele.next();
  if(ele.parent().attr('class') == 'filter-selected'){
    ele.appendTo($('.filter-tags .list-selectors'))
    value.appendTo($('.filter-tags .list-selectors'))
  } else {
    ele.appendTo($('.filter-selected'))
    value.appendTo($('.filter-selected'))
  }
}

// CLip post
function clip_post(){
  $('.clipjs').on('click',function(){
    if($(this).attr('class').includes('clipped')){
      $(this).removeClass('clipped');
    } else {
      $(this).addClass('clipped');
    }
  });
}

// Search

$('.search-btn').click(function(){
  let query = $('.search-text').val().trim();
  if(query) {
    window.location.href = window.location.origin.concat('/search/').concat(query);
  }
});
