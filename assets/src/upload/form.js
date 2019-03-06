import { doc } from '../utils'

const $fileField = doc('#id_file')[0]
$fileField.addEventListener('change', () => {
  const file = $fileField.files[0]
  const $fileFieldLabel = doc('span.file-label')[0]
  $fileFieldLabel.textContent = file.name
  $fileFieldLabel.insertAdjacentHTML('afterend','<i class="fas fa-spin fa-spinner"></i>');
})
