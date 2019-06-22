import Vue from 'vue/dist/vue.esm'
import axios from 'axios'

import { ready, ajaxForm, doc } from '../../utils'


ready(() => {
  const pointInput = new Vue({
    el: '#v-point-input',
    delimiters: ['[[', ']]'],
    data() {
      return {
        pointInput: 1,
        isLoading: false,
        points: [],
      }
    },
    computed: {
      pointSum() {
        let result = 0
        this.points.forEach(point => {
          result += point.count
        })
        return result
      }
    },
    mounted() {
      this.updatePointSum()
    },
    methods: {
      add(e) {
        e.preventDefault()
        this.pointInput++
      },
      minus(e) {
        e.preventDefault()
        if (this.pointInput > 1) {
          this.pointInput--
        }
      },
      preventTouch(e) {
        if (e.target.type !== 'submit') {
          e.preventDefault()
        }
      },
      hideModal() {
        this.$refs.pointModal.classList.remove('is-active')
      },
      updatePointSum() {
        const videoId = doc('video').dataset.videoId
        this.isLoading = true
        axios.get(`/ajax/points/list/${videoId}`)
          .then(response => {
            this.points = response.data.results
          })
          .finally(() => {
            this.isLoading = false
          })
      }
    }
  })
  ajaxForm('#point-form', () => {
    pointInput.hideModal()
    pointInput.pointInput = 1
    pointInput.updatePointSum()
  })
})
