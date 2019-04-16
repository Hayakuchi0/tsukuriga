import Vue from 'vue/dist/vue.esm'
import axios from 'axios'

import { ready, ajaxForm, doc } from '../../utils'


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
            let pointSum = 0
            response.data.results.forEach(point => {
              pointSum += point.count
            })
            this.pointSum = pointSum
          })
          .finally(() => {
            this.isLoading = false
          })
      }
    }
  })
  const pointForm = new Vue({
    el: '#v-point-modal',
    delimiters: ['[[', ']]'],
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
  ajaxForm('#point-form', () => {
    pointForm.hideModal()
    pointForm.pointInput = 1
    pointText.updatePointSum()
  })
})
