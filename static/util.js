function $(e) { return document.querySelector(e) }
Element.prototype.on = function (type, listener) { this.addEventListener(type, listener) }