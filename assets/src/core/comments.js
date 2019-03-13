import axios from 'axios'
import Vue from 'vue/dist/vue'

import { doc, ready } from '../utils'


ready(() => {
  /**
   * コメント単体のVueコンポーネント
   */
  Vue.component('v-comment-item', {
    template: '#v-comment-item',
    delimiters: ['[[', ']]'],
    props: ['comment']
  })

  /**
   * コメント一覧のVueコンポーネント
   */
  const commentList = new Vue({
    el: '#v-comment-list',
    data() {
      return {
        comments: []
      }
    },
    computed: {
      isEmpty() {
        return this.comments.length === 0
      }
    },
    mounted() {
      this.getComments()
    },
    methods: {
      getComments() {
        const videoId = doc('video')[0].dataset.videoId
        const self = this
        axios.get(`/ajax/comments/list/${videoId}`)
          .then(response => {
            self.comments = response.data.results
          })
      }
    }
  })

  /**
   * コメントフォーム
   */
  const $ajaxForm = doc('form.ajax-form')
  $ajaxForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=submit]')
    $form.addEventListener('submit', e => {
      e.preventDefault()

      $submitButton.disabled = true
      $submitButton.classList.add('is-loading')

      const formData = new FormData($form)
      $form.reset()

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
          commentList.getComments()
          $submitButton.classList.remove('is-loading')
          $submitButton.disabled = false
        })
    })
  })
})
