/*
  login.js
  
  Standard login view.
  
  When LoginView created, call intallUI to fetch the data and render the page.
  Also you can call unInstallUI to clear all the elements in container. Or 
  refreshUI to fetch data and render again.
  
  Author: Andy Zhau
*/

// Container is a div or some control of html to hold the rendered data.
// Data is a adaptor to fetch the request data.
function LoginView(container, data) {
  this.container = container;
  this.data = data;
}

LoginView.prototype.installUI = function(onDone, onError) {
  function onDone1(view) {
    view._installUIContinue();
    onDone();
  }
  
  function onError1(view, e) {
    view._installUIContinue();
    onDone();
  }
  this.data.fetchData(this, onDone1, onError1);
}

LoginView.prototype.refreshUI = function() {
  this.unInstallUI();
  this.installUI();
}

LoginView.prototype.unInstallUI = function() {
  this.container.innerHTML = "";
}

LoginView.prototype._installUIContinue = function() {
  this.unInstallUI();
  if (this.data.logined) {
    var htmlHolder = new HTMLHolder(
      '<div id="login" class="login-panel" title="Login">' +
  			'<span>欢迎您：</span>' + 
  			'<span class="login-user-name">\\0</span>' + 
  			'<span id="logout-btn"><a class="a-btn a-btn-m" tabindex="2"><span>退出</span></a></span>' +
  		'</div>'
    );
    var html = htmlHolder.getHTML([this.data.username]);
    this.container.innerHTML = html;
  } else {
    var htmlHolder = new HTMLHolder(
      '<div class="login-panel" title="Login">' +
        '<span><label for="login-user-name" class="login-text">用户名：</label></span>' +
			  '<span><input id="login-user-name" name="login-user-name" class="login-textbox" type="text"></input></span>' +
			  '<span><label for="login-user-password" class="login-text">密码：</label></span>' +
			  '<span><input id="login-user-password" name="login-user-password" class="login-textbox" type="password"></input></span>' +
			  '<span class="s-btn"><a id="login-btn" class="a-btn a-btn-m" tabindex="2"><span>登录</span></a></span>' +
			  '<span class="s-btn"><a id="register-btn" class="a-btn a-btn-m" tabindex="3"><span>注册</span></a></span>' +
			'</div>'
    )
    this.container.innerHTML = htmlHolder.getHTML([]);
  }
}
