(() => {
  'use strict'

  const kelvinEl = document.querySelector('#kelvin')
  const celsiusEl = document.querySelector('#celsius')

  kelvinEl.addEventListener('input', function () {
    celsiusEl.value = (parseFloat(this.value) - 273.15).toFixed(2)
  })

  celsiusEl.addEventListener('input', function () {
    kelvinEl.value = (parseFloat(this.value) + 273.15).toFixed(2)
  })
})()
