
try {
  new Function("import('/hacsfiles/frontend/main-a4943daf.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-a4943daf.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  