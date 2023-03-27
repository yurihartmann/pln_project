function openHelp(module, path, title, p_width, p_height) {
	var html = "http://www.furb.br/docsds/" + module + "/ajuda/" + path;
	var win = new Window({className:"alphacube", title:title, width:p_width, minimizable:true, maximizable:true, height:p_height, url:html});
	win.showCenter(false);
}

