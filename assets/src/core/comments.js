import axios from 'axios'
import Vue from 'vue/dist/vue'

import { doc, ready, ajaxForm } from '../utils'


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
  ajaxForm('#comment-form', () => {
    commentList.getComments()
  })
})
