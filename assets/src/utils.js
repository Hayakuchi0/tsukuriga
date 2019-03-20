import axios from 'axios'

export const ready = callback => document.addEventListener('DOMContentLoaded', callback)

export const doc = q => Array.from(document.querySelectorAll(q))

export const range = n => [...Array(n).keys()]

export const ajaxForm = (callback, reset) => {
  const $ajaxForm = doc('form.ajax-form')
  $ajaxForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=submit]')
    $form.addEventListener('submit', e => {
      e.preventDefault()

      $submitButton.disabled = true
      $submitButton.classList.add('is-loading')

      const formData = new FormData($form)
      if (reset) {
        $form.reset()
      }

      axios.post($form.action, formData)
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
          callback()
          $submitButton.classList.remove('is-loading')
          $submitButton.disabled = false
        })
    })
  })
}
