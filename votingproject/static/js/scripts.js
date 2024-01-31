/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// THIS IS FOR THE STICKY HEADER

 // When the user scrolls, call the function
 window.onscroll = function() {
    stickyHeader();
  };

  // Get the header
  var nav = document.getElementById("navbr");

  // Get the offset position of the header
  var sticky = nav.offsetTop;

  // Add the sticky class to the header when you reach its scroll position
  // Remove "sticky" when you leave the scroll position
  function stickyHeader() {
    if (window.pageYOffset > sticky) {
      nav.classList.add("sticky");
    } else {
      nav.classList.remove("sticky");
    }
  }






    
// $(function() {
//     var nav = $(".navbar");
//       $(window).scroll(function() {
//         var scroll = $(window).scrollTop();
//         if (scroll >= 200) {
//             nav.addClass("sticky-menu");
//       } else {
//           nav.removeClass('sticky-menu');
//         }
//       });
//   });
  
  
//   $(window).scroll(function(){
  
//   // Variables
//   var $body = $(".sticky-menu");
//   var windowScrollTop = $(window).scrollTop();
//   var scroll = $(window).scrollTop();
//   if (scroll >= 50) {
//     $body.addClass("active");
//   } else {
//     $body.removeClass('active');
//   }
//   });