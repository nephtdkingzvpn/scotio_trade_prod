document.addEventListener("DOMContentLoaded", function() {
    var navLinks = document.querySelectorAll(".aside__links .side__link");
    var currentPath = window.location.pathname;
  
    navLinks.forEach(function(link) {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
      }
    });
});



// togle sidebar
const closeBtn = document.querySelector('#sidebar-close-btn');
const menuBtn = document.querySelector('#menu-bar');
const sidebar = document.querySelector('aside');

menuBtn.addEventListener('click', ()=>{
  sidebar.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
  sidebar.style.display = 'none';
});


















// document.addEventListener("DOMContentLoaded", function() {
//   var navLinks = document.querySelectorAll(".aside__links .side__link");

//   navLinks.forEach(function(link) {
//     link.addEventListener("click", function(event) {
//       // Prevent default link behavior (e.g., following href)
//     //   event.preventDefault();

//       // Remove active class from all links
//       navLinks.forEach(function(link) {
//         link.classList.remove("active");
//       });

//       // Add active class to the clicked link
//       link.classList.add("active");
//     });
//   });
// });

