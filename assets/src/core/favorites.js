import Vue from 'vue/dist/vue.esm'

import { doc, ready, csrf, Notify } from '../utils'
import axios from 'axios'


ready(() => {
  new Vue({
    el: '#v-favorite-button',
    delimiters: ['[[', ']]'],
    data() {
      return {
        sumFavorites: 0,
        isCreated: false,
        isLoading: false
      }
    },
    mounted() {
      this.getFavorites()
    },
    computed: {
      className() {
        return 'button' +
          (this.isCreated ? ' is-primary' : '') +
          (this.isLoading ? ' is-loading' : '')
      },
      iconClassName() {
        return (this.isCreated ? 'fas fa-minus-square' : 'fas fa-plus-square') + ' with-text'
      }
    },
    methods: {
      getFavorites() {
        const videoId = doc('video')[0].dataset.videoId
        const self = this

        this.isLoading = true
        axios.get(`/ajax/favorites/list/${videoId}`)
          .then(response => {
            self.sumFavorites = response.data.results.favorites.length
            self.isCreated = response.data.results.isCreated
          })
          .finally(() => {
            self.isLoading = false
          })
      },
      toggleFavorite() {
        const videoId = doc('video')[0].dataset.videoId
        axios.post(`/ajax/favorites/toggle/${videoId}`, csrf())
          .then(response => {
              Notify.activate('success', response.data.results.message)
              this.getFavorites()
            }
          )
      }
    }
  })
})
