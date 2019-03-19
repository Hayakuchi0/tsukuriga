import { doc, ready, ajaxForm } from '../utils'


ready(() => {
  ajaxForm(() => {
    doc('#point-modal')[0].classList.remove('is-active')
  })
})
