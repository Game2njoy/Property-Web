(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Fixed Navbar
    // jQuery를 사용하여 window 객체에 스크롤 이벤트 리스너를 추가합니다.
    $(window).scroll(function () {
        // 브라우저 창의 너비가 992픽셀 미만인 경우의 조건을 체크합니다.
        if ($(window).width() < 992) {
            // 사용자가 45픽셀 이상 스크롤 했는지 여부를 체크합니다.
            if ($(this).scrollTop() > 45) {
                // 45픽셀 이상 스크롤 했다면, '.fixed-top' 클래스를 가진 요소에 'bg-white'와 'shadow' 클래스를 추가합니다.
                // 이는 해당 요소에 흰색 배경과 그림자 효과를 적용하기 위함입니다.
                $('.fixed-top').addClass('bg-white shadow');
            } else {
                // 45픽셀 미만으로 스크롤 했다면, '.fixed-top' 요소로부터 'bg-white'와 'shadow' 클래스를 제거합니다.
                $('.fixed-top').removeClass('bg-white shadow');
            }
        } else {
            // 브라우저 창의 너비가 992픽셀 이상인 경우
            // 사용자가 45픽셀 이상 스크롤 했는지 여부를 체크합니다.
            if ($(this).scrollTop() > 45) {
                // 45픽셀 이상 스크롤 했다면, '.fixed-top' 클래스를 가진 요소에 'bg-white'와 'shadow' 클래스를 추가하고,
                // CSS의 'top' 속성값을 '-45'로 설정합니다. 이는 요소를 위로 45픽셀 올리는 효과를 줍니다.
                $('.fixed-top').addClass('bg-white shadow').css('top', 0);
            } else {
                // 45픽셀 미만으로 스크롤 했다면, '.fixed-top' 요소로부터 'bg-white'와 'shadow' 클래스를 제거하고,
                // 'top' 속성값을 '0'으로 재설정합니다. 이는 요소의 위치를 원래대로 복원합니다.
                $('.fixed-top').removeClass('bg-white shadow').css('top', 0);
            }
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
            $('.dropup').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
            $('.dropup').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 500, 'easeInOutExpo');
        return false;
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        loop: true,
        center: true,
        dots: false,
        nav: true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });

    
})(jQuery);

