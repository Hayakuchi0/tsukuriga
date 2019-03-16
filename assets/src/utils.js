export const ready = callback => document.addEventListener('DOMContentLoaded', callback)

export const doc = q => document.querySelectorAll(q)

export const range = n => [...Array(n).keys()]
