import Vue from 'vue/dist/vue'

import { doc, ready, ajaxForm } from '../utils'


ready(() => {
  const pointForm = new Vue({
    el: '#v-point-modal',
    data() {
      return {
        pointInput: 1
      }
    }
  })
  ajaxForm(() => {
    pointForm.$refs.pointModal.classList.remove('is-active')
  })
})
