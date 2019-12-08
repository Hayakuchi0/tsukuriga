import { ready, doc, docAll } from '../utils'
import browser from 'browser-detect'

const templates = {
  suggestion: `[提案]
* 提案内容
(提案内容を簡潔に分かりやすく書いてください)

* なぜ上記提案が必要か
(提案内容によって解決できる現状の問題、提案内容によって得られる嬉しいこと など詳しく)

`,
  issue: `[不具合報告]
* 不具合が発生するページ
(URLを貼ってください)

* 不具合の内容
(発生した経緯、頻度など情報は多ければ多いほど助かります)

* 他のブラウザでは動作したか
(はい/いいえ/分からない)

* ブラウザのキャッシュを消して改善したか
(はい/いいえ/分からない)
`
}

ready(() => {
  const $uaInput = doc('#id_ua')
  $uaInput.value = JSON.stringify(browser())

  const $textInput = doc('#id_text')
  let templateId = location.hash.substring(1)
  if (templateId) {
    $textInput.value = templates[templateId]
  }

  docAll('[data-action=insert-template]').forEach($anchor => {
    $anchor.addEventListener('click', e => {
      templateId = $anchor.dataset.templateId
      $textInput.value = templates[templateId]
    })
  })
})
