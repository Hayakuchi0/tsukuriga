import { doc, ready } from '../utils'

ready(() => {
  const $submitForm = doc('form')
  $submitForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=button]')
    $submitButton.addEventListener('click', e => {
      doc('#id_time')[0].value = doc('video')[0].currentTime
      $submitButton.classList.add('is-loading')
      $submitButton.disabled = true
      $form.submit()
    })
  })
})
