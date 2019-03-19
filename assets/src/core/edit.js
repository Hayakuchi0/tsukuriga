import Vue from 'vue/dist/vue'

import { doc, ready } from '../utils'


ready(() => {
  new Vue({
    el: '#v-delete-modal',
    data() {
      return {
        deleteInput: '',
        correctInput: ''
      }
    },
    mounted() {
      const $modal = this.$refs.deleteModal
      this.correctInput = $modal.dataset.videoId
      this.$refs.background.addEventListener('click', e => {
        $modal.classList.remove('is-active')
      })
    },
    computed: {
      isDeletable() {
        return this.deleteInput === this.correctInput
      }
    }
  })
})
