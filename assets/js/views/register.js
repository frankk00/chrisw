/*
  register.js
  
  Standard register view.
  
  When LoginView created, call intallUI to fetch the data and render the page.
  Also you can call unInstallUI to clear all the elements in container. Or 
  refreshUI to fetch data and render again.
  
  Author: Andy Zhau
*/

// Container is a div or some control of html to hold the rendered data.
// Data is a adaptor to fetch the request data.
function RegisterView(container, data) {
  this._container = container;
  this._data = data;
}

RegisterView.prototype.installUI = function(onDone, onError) {
  this._installUIContinue();
  onDone();
}

RegisterView.prototype.refreshUI = function() {
  this.unInstallUI();
  this.installUI();
}

RegisterView.prototype.unInstallUI = function() {
  this._container.innerHTML = "";
}

RegisterView.prototype._installUIContinue = function() {
  this.unInstallUI();
  var htmlHolder = new HTMLHolder(
    '<span>欢迎来到倒时差网站，只需简单信息即可完成注册：</span>' + 
    '<div id="register-panel" class="info-panel">'+
			'<table class="info-table">'+
				'<tbody>'+
					'<tr>'+
						'<td class="info-label">'+
							'<span>用户名</span>'+
						'</td>'+
						'<td class="info-content">'+
							'<input id="username-text" type="text" />'+
						'</td>'+
					'</tr>'+
					'<tr>'+
						'<td class="info-label">'+
							'<span>昵称</span>'+
						'</td>'+
						'<td class="info-content">'+
							'<input id="fullname-text" type="text" />'+
						'</td>'+
					'</tr>'+
					'<tr>'+
						'<td class="info-label">'+
							'<span>密码</span>'+
						'</td>'+
						'<td>'+
							'<input id="password-text" type="password" />'+
						'</td>'+
					'</tr>'+
					'<tr>'+
						'<td class="info-label">'+
							'<span>邮箱</span>'+
						'</td>'+
						'<td class="info-content">'+
							'<input id="email-text" type="text" />'+
						'</td>'+
					'</tr>'+
					'<tr>'+
						'<td colspan="2" class="bottom-btn">'+
							'<span id="logout-btn"><a class="a-btn a-btn-m" tabindex="2"><span>注册</span></a></span>'+
						'</td>'+
					'</tr>'+
				'</tbody>'+
			'</table>'+
		'</div>'+
	'</div>'
  );
  var html = htmlHolder.getHTML([]);
  this._container.innerHTML = html;
}
