import Vue from 'vue/dist/vue.esm'

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
    },
    computed: {
      isDeletable() {
        return this.deleteInput === this.correctInput
      }
    },
    methods: {
      hideModal() {
        this.$refs.deleteModal.classList.remove('is-active')
      }
    }
  })
})
