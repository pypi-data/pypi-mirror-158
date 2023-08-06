
try {
  new Function("import('/hacsfiles/frontend/main-dc658e23.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-dc658e23.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  