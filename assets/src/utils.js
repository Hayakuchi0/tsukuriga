import Vue from 'vue/dist/vue'

export const ready = callback => document.addEventListener('DOMContentLoaded', callback)

export const vue_component = options => {
  ready(() => {
    options.delimiters = ['[[', ']]']
    new Vue(options)
  })
}

export const doc = q => document.querySelectorAll(q)
