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
      },
      sortedPoints() {
        let results = []
        this.points.forEach(point => {
          const key = point.user ? point.user.username : point.username
          let hasKey = false
          results.forEach(item => {
            if (item.username === key) {
              item.count += point.count
              hasKey = true
            }
          })
          if (!hasKey) {
            results.push({username: key, user: point.user, count: point.count})
          }
        })
        return results.sort((a, b) => a.count > b.count ? -1 : 1).slice(0, 5)
      }
    },
    mounted() {
      this.updatePoints()
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
      updatePoints() {
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
    pointInput.updatePoints()
  })
})
