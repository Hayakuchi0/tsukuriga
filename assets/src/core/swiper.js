import Swiper from 'swiper'

new Swiper('.swiper-container', {
  loop: true,
  autoplay: {
    delay: 7000,
  },
  pagination: {
    el: '.swiper-pagination',
  },
})
