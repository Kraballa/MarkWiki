function $(e) { return document.querySelector(e) }
function $$(e) {return document.querySelectorAll(e)}
Element.prototype.on = function (type, listener) { this.addEventListener(type, listener) }

$$(".content input[type=checkbox].semi").forEach((cb) => {
    cb.indeterminate = true;
})