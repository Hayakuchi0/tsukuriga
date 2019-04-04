import Tooltip from 'tooltip.js'

import { doc, ready, Notify } from '../utils'
import './styles.scss'


ready(() => {
  /**
   * ファイル入力フィールド用処理
   *
   */
  const $fileField = doc('input[type=file]')
  $fileField.forEach($field => {
    $field.addEventListener('change', () => {
      const file = $field.files[0]
      const $fieldName = $field.parentNode.querySelector('span.file-name')
      $fieldName.textContent = file.name
    })
  })


  /**
   * 2重サブミット対策
   *
   */
  const $submitForm = doc('form.submit-form')
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
  const $modalButton = doc('.modal-opener')
  $modalButton.forEach($button => {
    const modalId = $button.dataset.target
    $button.addEventListener('click', e => {
      doc('#' + modalId)[0].classList.add('is-active')
    })
  })

  /**
   * ツイートボタン
   */
  doc('.tweet-button').forEach($button => {
    const text = $button.dataset.text || document.title
    const url = location.origin + $button.dataset.href || location.pathname
    const hashtags = $button.dataset.hashtags || 'tsukuriga'
    $button.href = `https://twitter.com/intent/tweet?text=${text}&url=${url}&hashtags=${hashtags}`
    $button.onclick = e => {
      window.open(
        encodeURI(decodeURI($button.href)), 'ツイート',
        'width=650, height=270, personalbar=0, toolbar=0, scrollbars=1, sizable=1'
      )
      return false
    }
  })

  /**
   * 通知用
   */
  doc('.notify-data').forEach(notification => {
    Notify.activate(notification.dataset.tag, notification.dataset.message)
  })

  /**
   * トロフィーポップアップ用
   */
  doc('.tooltipRef').forEach($tooltip => {
    new Tooltip($tooltip, {
      title: $tooltip.dataset.tooltip,
      placement: 'bottom',
    })
  })
})
