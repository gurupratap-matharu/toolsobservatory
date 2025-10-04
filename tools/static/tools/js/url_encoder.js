(() => {
  'use strict'

  const inputEl = document.querySelector('#input')
  const outputEl = document.querySelector('#output')

  inputEl.addEventListener('input', function () {
    outputEl.textContent = encodeURIComponent(inputEl.value)
  })

  function copy () {
    const copyText = document.querySelector('#output')
    copyText.select()
    document.execCommand('copy')
  }

  document.querySelector('#copy').addEventListener('click', copy)
})()
