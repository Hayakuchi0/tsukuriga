import Vue from 'vue/dist/vue'

export const vue_component = options => {
  document.addEventListener('DOMContentLoaded', () => {
    options.delimiters = ['[[', ']]']
    new Vue(options)
  })
}

export const doc = q => document.querySelectorAll(q)
