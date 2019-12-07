import { ready, doc } from '../utils'
import browser from 'browser-detect'

ready(() => {
  const $uaInput = doc('#id_ua')
  $uaInput.value = JSON.stringify(browser())
  $uaInput.style = 'background-color: #b5b5b5 !important'
})
