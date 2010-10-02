var leftPanel;
var rightPanel;
var detailPanel;

$(window).ready(function() {
  renderRightPanel();
  renderDetailPanel();
  
  leftPanel = new StandardPanel($("#left-panel")[0]);
})

function renderRightPanel() {
  var layout = new VerticalLayout($("#right-panel")[0]);
  rightPanel = new StandardPanel(layout);
  var loginView = new LoginView(layout.registView(), new LoginDataAdaptor());
  loginView.installUI(function() {
    layout.appendView("login", loginView);
    bindingLogin();
  });
}

function renderDetailPanel() {
  var layout = new VerticalLayout($("#detail-content")[0]);
  detailPanel = new SlidePanel("detail-panel", layout);
  
  $("#detail-panel-close").click(function() {
    detailPanel.hide("");
  })
}

function bindingLogin() {
  $("#login-btn").click(function() {
    login($("#login-user-name").val(), $("#login-user-password").val(), function() {
      rightPanel.layout.findView("login").installUI(bindingLogin);
    });
  })

  $("#logout-btn").click(function() {
    logout(function() {
      rightPanel.layout.findView("login").installUI(bindingLogin);
    });
  })
  
  $("#register-btn").click(function() {
    renderRegister(function() {
      detailPanel.click("detail");
    });
  })
}

function renderRegister(onDone) {
  detailPanel.layout.removeAll();
  var registerView = new RegisterView(detailPanel.layout.registView());
  registerView.installUI(function() {
    onDone();
  })
}

function renderGroup(groupid, offset, limit) {
  JsonpQueue.call(
    "/group/" + groupid,
    {},
    renderGroupSuccess
  )
}

function renderGroupSuccess(data) {
  leftView = new GroupView(data.action.data);
  leftView.installUI($("#left-panel")[0]);
  $("#group-title").click(clickGroupInfo);
}

function clickGroupInfo() {
  if (detailTitle == "group_info") {
    hideDetailPanel(function() {
      detailView.unInstallUI();
      detailTitle = null;      
    });
  } else {
    if (detailView != null) {
      detailView.unInstallUI();
    }
    detailView = new GroupView(leftView.data);
    detailView.installUI($("#detail_panel")[0]);
    showDetailPanel();
    detailTitle = "group_info";
  }    
}

function renderLogin() {
  var data = new LoginDataAdaptor();
  leftView = new LoginView($("#left-panel")[0], data);
  
  leftView.installUI(function() {
    
  });
}