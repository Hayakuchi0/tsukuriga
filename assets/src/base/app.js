import { doc, ready } from '../utils'
import './styles.scss'


ready(() => {
  /**
   * メニュー開閉
   * https://bulma.io/documentation/components/navbar/#navbar-menu
   */
  const $navbarBurger = doc('.navbar-burger')[0]
  $navbarBurger.addEventListener('click', (e) => {
    doc('.navbar-burger')[0].classList.toggle('is-active')
    doc('.navbar-menu')[0].classList.toggle('is-active')
  })

  /**
   * Notyf
   * https://github.com/caroso1222/notyf
   */
  const notyf = new Notyf({
    delay: 5000
  })
  const notyf_key = {
    success: 'confirm',
    error: 'alert'
  }
  doc('.notyf-data').forEach(data => {
    notyf[notyf_key[data.dataset.tags]](data.dataset.message)
  })

  /**
   * ファイル入力フィールド用処理
   *
   */
  const $fileField = doc('input[type=file]')
  $fileField.forEach($field => {
    $field.addEventListener('change', () => {
      const file = $field.files[0]
      const $fieldLabel = $field.nextElementSibling.querySelector('span.file-label')
      $fieldLabel.textContent = file.name
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
    const hashtags = $button.dataset.hashtags || 'ハッシュタグ'
    $button.href = `https://twitter.com/intent/tweet?text=${text}&url=${url}&hashtags=${hashtags}`
    $button.onclick = e => {
      window.open(
        encodeURI(decodeURI($button.href)), 'ツイート',
        'width=650, height=270, personalbar=0, toolbar=0, scrollbars=1, sizable=1'
      )
      return false
    }
  })
})
