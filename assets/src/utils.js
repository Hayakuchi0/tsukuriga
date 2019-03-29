import Vue from 'vue/dist/vue.esm'
import axios from 'axios'

export const ready = callback => document.addEventListener('DOMContentLoaded', callback)

export const doc = q => Array.from(document.querySelectorAll(q))

export const range = n => [...Array(n).keys()]

export const ajaxForm = (form, callback) => {
  const $ajaxForm = doc(form)
  $ajaxForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=submit]')
    $form.addEventListener('submit', e => {
      e.preventDefault()

      $submitButton.disabled = true
      $submitButton.classList.add('is-loading')

      const formData = new FormData($form)
      $form.reset()

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

export const fadeIn = el => {
  /**
   * http://youmightnotneedjquery.com/
   */
  el.style.opacity = 0

  let last = +new Date()
  const tick = () => {
    el.style.opacity = +el.style.opacity + (new Date() - last) / 400
    last = +new Date()

    if (+el.style.opacity < 1) {
      (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16)
    }
  }

  tick()
}

export const Notify = () => new Vue({
  el: '#notify-container',
  delimiters: ['[[', ']]'],
  computed: {
    hasNotify() {
      return this.tag && this.message
    },
    className() {
      if (this.hasNotify) {
        return 'notification is-' + this.tag
      }
    }
  },
  data() {
    return {
      tag: '',
      message: ''
    }
  },
  methods: {
    activate(tag, message) {
      fadeIn(this.$refs.notifyItem)
      this.tag = tag
      this.message = message
    },
    deactivate() {
      this.tag = ''
      this.message = ''
    }
  }
})
