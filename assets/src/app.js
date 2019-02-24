import * as toastr from 'toastr'
import './styles.scss'

document.addEventListener('DOMContentLoaded', () => {
  const $ = q => document.querySelectorAll(q)

  /**
   * メニュー開閉
   * https://bulma.io/documentation/components/navbar/#navbar-menu
   */
  const $navbarBurger = $('.navbar-burger')[0]
  $navbarBurger.addEventListener('click', (e) => {
    $('.navbar-burger')[0].classList.toggle('is-active')
    $('.navbar-menu')[0].classList.toggle('is-active')
  })

  /**
   * toastr.js用
   */
  toastr.options = {
    'positionClass': 'toast-bottom-right',
  }
  $('.toastr-data').forEach(data => {
    toastr[data.dataset.tags](data.dataset.message)
  })
})
