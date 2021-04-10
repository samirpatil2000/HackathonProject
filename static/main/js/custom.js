new WOW().init();

// mobile menu open close
function openNav() {
  document.getElementById("mySidenav").style.left = "0";
}

function closeNav() {
  document.getElementById("mySidenav").style.left = "-100%";
}


// Chapter slider
$('.course .owl-carousel').owlCarousel({
    stagePadding: 50,
    loop:true,
    margin:20,
    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause: true,
    nav:true,
    navText:["<span class='fas fa-chevron-left'></span>","<span class='fas fa-chevron-right'></span>"],
    dots:true,
    responsive:{
        0:{
            items:1,
            margin:10,
        },
        600:{
            items:2,
            dots: false,
            stagePadding: 0,
        },
        1000:{
            items:3
        },
        1200:{
            items:4
        }
    }
});


$('.client-slide .owl-carousel').owlCarousel({
    loop:true,
    margin:30,
    nav:false,
    navText:["<span class='fal fa-arrow-left'></span>","<span class='fal fa-arrow-right'></span>"],
    dots:true,
    responsive:{
        0:{
            items:2,
        },
        600:{
            items:2,
        },
        768:{
            items:3,            
        },
        1000:{
            items:6,
        },
        1501:{
            items:6
        }
    }
});



jQuery(document).ready(function ($) {
  $('#pills-tab[data-mouse="hover"] a').hover(function(){
    $(this).tab('show');
  });
  $('a[data-toggle="pill"]').on('shown.bs.tab', function (e) {
    var target = $(e.relatedTarget).attr('href');
    $(target).removeClass('active');
  })
});

$(document).ready(function(){
  $(".schedule-btn a").click(function(){
    //$("#schedule-form").fadeOut(250).fadeIn(250);
    $("#schedule-form").css('border', 'solid 4px #114cd1'); 
  });
});
