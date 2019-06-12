import Tooltip from 'tooltip.js'

import { doc, docAll, ready, activateTweetButton, Notify } from '../utils'
import './styles.scss'


ready(() => {
  /**
   * 2重サブミット対策
   *
   */
  const $submitForm = docAll('form.submit-form')
  $submitForm.forEach($form => {
    const $submitButton = $form.querySelector('button[type=submit]')
    $form.addEventListener('submit', e => {
      $submitButton.classList.add('is-loading')
      $submitButton.disabled = true
    })
  })

  /**
   * モーダル展開
   */
  const $modalButton = docAll('.modal-opener')
  $modalButton.forEach($button => {
    const modalId = $button.dataset.target
    $button.addEventListener('click', e => {
      doc('#' + modalId).classList.add('is-active')
    })
  })
  const $modalBg = docAll('.modal-closer')
  $modalBg.forEach($bg => {
    $bg.addEventListener('click', e => {
      $bg.parentNode.classList.remove('is-active')
    })
  })

  /**
   * ツイートボタン
   */
  docAll('.tweet-button').forEach(activateTweetButton)

  /**
   * 通知用
   */
  docAll('.notify-data').forEach(notification => {
    Notify.activate(notification.dataset.tag, notification.dataset.message)
  })

  /**
   * トロフィーポップアップ用
   */
  docAll('.tooltipRef').forEach($tooltip => {
    new Tooltip($tooltip, {
      title: $tooltip.dataset.tooltip,
      placement: 'bottom',
    })
  })
})
