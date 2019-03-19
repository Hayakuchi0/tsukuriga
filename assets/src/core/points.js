import Vue from 'vue/dist/vue'
import axios from 'axios'

import { ready, ajaxForm, doc } from '../utils'


ready(() => {
  const pointText = new Vue({
    el: '#v-point-text',
    delimiters: ['[[', ']]'],
    data() {
      return {
        isLoading: false,
        pointSum: 0
      }
    },
    mounted() {
      this.updatePointSum()
    },
    methods: {
      updatePointSum() {
        const videoId = doc('video')[0].dataset.videoId
        this.isLoading = true
        axios.get(`/ajax/points/list/${videoId}`)
          .then(response => {
            this.pointSum = response.data.results[0].count
          })
          .finally(() => {
            this.isLoading = false
          })
      }
    }
  })
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
    pointForm.pointInput = 1
    pointText.updatePointSum()
  })
})
