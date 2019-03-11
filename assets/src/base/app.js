import { doc, ready } from '../utils'
import Notyf from 'notyf'

import 'notyf/dist/notyf.min.css'
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
   * Notyf
   * https://github.com/caroso1222/notyf
   */
  const notyf = new Notyf()
  const notyf_key = {
    success: 'confirm',
    error: 'alert'
  }
  doc('.notyf-data').forEach(data => {
    notyf[notyf_key[data.dataset.tags]](data.dataset.message)
  })

  /**
   * ファイル入力フィールド用処理
   *
   */
  const $fileField = doc('input[type=file]')
  $fileField.forEach($field => {
    $field.addEventListener('change', () => {
      const file = $field.files[0]
      const $fieldLabel = $field.nextElementSibling.querySelector('span.file-label')
      $fieldLabel.textContent = file.name
    })
  })


  /**
   * 2重サブミット対策
   *
   */
  const isSubmitting = false
  const $submitForm = doc('form')
  $submitForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=submit]')
    $form.addEventListener('submit', e => {
      if (isSubmitting) {
        e.preventDefault()
      } else {
        $submitButton.classList.add('is-loading')
      }
    })
  })
})
