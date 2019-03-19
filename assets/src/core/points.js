import Vue from 'vue/dist/vue'

import { doc, ready, ajaxForm } from '../utils'


ready(() => {
  const pointForm = new Vue({
    el: '#v-point-modal',
    data() {
      return {
        pointInput: 1
      }
    },
    methods: {
      add() {
        this.pointInput++
      },
      minus() {
        if (this.pointInput > 1) {
          this.pointInput--
        }
      },
      hideModal() {
        this.$refs.pointModal.classList.remove('is-active')
      }
    }
  })
  ajaxForm(() => {
    pointForm.hideModal()
  })
})
