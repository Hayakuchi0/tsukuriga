import axios from 'axios'
import Notyf from 'notyf'

import { doc } from '../utils'


const $ajaxForm = doc('form.ajax-form')
$ajaxForm.forEach($form => {
  const $submitButton = $form.querySelector('button[type=submit]')
  $form.addEventListener('submit', e => {
    e.preventDefault()

    $form.reset()
    $submitButton.disabled = true
    $submitButton.classList.add('is-loading')

    const formData = new FormData($form)
    axios.post($form.target, formData)
      .then(response => {
        const notyf = new Notyf({
          delay: 5000
        })
        if (response.data.isSuccess) {
          response.data.results.forEach(result => {
            notyf.confirm(result.message)
          })
        }
      })
      .finally(() => {
        $submitButton.classList.remove('is-loading')
        $submitButton.disabled = false
      })
  })
})
