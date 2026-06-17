// ImbirPay — Google Apps Script Web App
// Этот файл разворачивает приложение как веб-сайт

function doGet() {
  return HtmlService
    .createHtmlOutputFromFile('index')
    .setTitle('ImbirPay — Казначейство Imbir Group')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0');
}
