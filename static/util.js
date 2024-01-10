function $(e) { return document.querySelector(e) } // $("input[name=tab]:checked")
Element.prototype.on = function (type, listener) { this.addEventListener(type, listener) }