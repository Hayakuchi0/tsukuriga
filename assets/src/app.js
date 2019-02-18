import './styles.scss'

$(document).ready(() => {

  /**
   * メニュー開閉
   * https://bulma.io/documentation/components/navbar/#navbar-menu
   */
  $('.navbar-burger').click(() => {
    $('.navbar-burger').toggleClass('is-active')
    $('.navbar-menu').toggleClass('is-active')
  })

  /**
   * data-counted属性の付いたフォームに文字数カウンタ追加
   * /create
   */
  $('*[data-counted]')
    .after(
      `<div class="counter has-text-right"> </div>`
    )
    .on('keydown keyup keypress change', function() {
      const strLength = $(this).val().length
      const stateText =
        strLength !== 0 ?
          strLength + '/' + $(this).attr('maxlength') : ''
      $(this).next('.counter').text(stateText)
    })

})
