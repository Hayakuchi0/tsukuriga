import { ready, doc } from '../utils'

ready(() => {
  const $submitForm = doc('form')
  $submitForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=button]')
    $submitButton.addEventListener('click', e => {
      doc('#id_time')[0].value = doc('video')[0].currentTime
      $form.submit()
    })
  })
})
