import * as toastr from 'toastr'

import { doc, ready } from '../utils'
import './styles.scss'

ready(() => {
  /**
   * メニュー開閉
   * https://bulma.io/documentation/components/navbar/#navbar-menu
   */
  const $navbarBurger = doc('.navbar-burger')[0]
  $navbarBurger.addEventListener('click', (e) => {
    doc('.navbar-burger')[0].classList.toggle('is-active')
    doc('.navbar-menu')[0].classList.toggle('is-active')
  })

  /**
   * toastr.js用
   * 廃止予定
   */
  toastr.options = {
    'positionClass': 'toast-bottom-right',
  }
  doc('.toastr-data').forEach(data => {
    toastr[data.dataset.tags](data.dataset.message)
  })
})
