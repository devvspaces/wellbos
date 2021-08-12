$(document).ready(function(){
	// $(".et-preloader").fadeOut("slow");
	
	
	// Hero carosel
	$('.owl-carousel').owlCarousel({
		autoplay: true,
		loop:true,
		// margin:10,
		// nav:true,
		items: 1
	})

	$('.nav_search input').on('focus', function(){
		$('.nav_search').addClass('active')
	})

	$('.nav_search input').on('blur', function(){
		$('.nav_search').removeClass('active')
	})

	$('.nav_link').on('mouseover', function(){
		$(this.parentElement).addClass('active').siblings().removeClass('active')
		$('body').css('overflow', 'hidden')
	})

	$('.nav_backdrop').on('mouseover', function(e) {
		if (e.target.classList.contains('nav_backdrop')){
			$(this.parentElement).removeClass('active')
			$('body').css('overflow', 'auto')
		}
	})

	// $('.nav_backdrop').on('blur', function(e) {
	// 	// $(this.parentElement).removeClass('active')
	// })

	function resetView(){
		if (window.innerWidth > 627){
			$("#desktop").css('display', 'block')
			$("#mobile").css('display', 'none')
		} else {
			$("#desktop").css('display', 'none')
			$("#mobile").css('display', 'block')
		}
	}
	resetView()

	$(window).on('resize', function(){
		resetView()
	})

	$('.show-more a').click(function(e){
		e.preventDefault()
		if ($('.product-description').hasClass('active')){
			$('.product-description').removeClass('active')
			$('.show-more a').text('show less')
		} else {
			$('.product-description').addClass('active')
			$('.show-more a').text('show more')
		}
	})
})

console.clear()

const navExpand = [].slice.call(document.querySelectorAll('.nav-expand'))
const backLink = `<li class="nav-item">
	<a class="nav-link nav-back-link" href="javascript:;">
		Back
	</a>
</li>`

navExpand.forEach(item => {
	item.querySelector('.nav-expand-content').insertAdjacentHTML('afterbegin', backLink)
	item.querySelector('.nav-link').addEventListener('click', () => item.classList.add('active'))
	item.querySelector('.nav-back-link').addEventListener('click', () => item.classList.remove('active'))
})


// ---------------------------------------
// not-so-important stuff starts here

const ham = document.getElementById('ham')
ham.addEventListener('click', function() {
	document.body.classList.toggle('nav-is-toggled')
})
