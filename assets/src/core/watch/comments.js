import axios from 'axios'
import Vue from 'vue/dist/vue.esm'

import { doc, ready, user, csrf, getTweetHref, getTweetOnClick, Notify, ajaxForm } from '../../utils'


ready(() => {
  /**
   * コメント単体のVueコンポーネント
   */
  Vue.component('v-comment-item', {
    template: '#v-comment-item',
    delimiters: ['[[', ']]'],
    props: ['comment'],
    data() {
      return {
        user: user()
      }
    },
    computed: {
      tweetText() {
        return `【コメントしました】${this.comment.text.replace(/\s+/g, ' ')}\n`
      },
      tweetHref() {
        return getTweetHref(this.tweetText)
      },
      tweetOnClick() {
        return getTweetOnClick(this.tweetHref)
      }
    },
    methods: {
      deleteComment() {
        axios.post(`/ajax/comments/delete/${this.comment.id}`, csrf())
          .then(response => {
            if (response.data.isSuccess) {
              response.data.results.forEach(result => {
                Notify.activate('success', result.message)
              })
            }
          })
          .finally(() => {
            commentList.getComments()
          })
      },
      addReplyTarget() {
        // 匿名コメントに対応。ただしURLに置換はしない
        let target = `@${this.comment.username || this.comment.name}`
        let textArea = doc('#comment-form #id_text')
        textArea.value = target + '\n' + textArea.value
        textArea.focus()
      }
    }
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
        const videoId = doc('video').dataset.videoId
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
