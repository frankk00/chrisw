$(window).ready(function() {
  
  $.debug(true);
  $.log("psdfasd");

  // $("#login").dialog({
  //     disabled: true,
  //     modal: true,
  //     position: 'center',
  //     minHeight: 150,
  //     minWidth: 400,
  //     buttons: {
  //       Login: login,
  //       Cancel: function() {
  //         $(this).dialog('close');
  //       }
  //     }
  //   });
  
  // $("#login").dialog('close');
  // 
  // $("#login_span").click(function() {
  //   loadLoginPart();
  //   $("#login").dialog('open');
  // })
  // 
  // $("#logout_span").click(logout);
  
  renderGroup(1);
})

var leftView = null;
var detailView = null;

function loadLoginPart() {
  $("#login")[0].innerHTML = '<table border="0" cellspacing="5" cellpadding="5"><tbody><tr><th><label for="id_uid">Uid:</label></th><td><input type="text" name="uid" id="id_uid"></td></tr> <tr><th><label for="id_password">Password:</label></th><td><input type="text" name="password" id="id_password"></td></tr>    		</tbody></table>';
}

function login() {
  var backUrl = location.href;
  var pos = backUrl.indexOf("#");
  if (pos != -1) {
    backUrl = backUrl.substr(0, pos);
  }
  JsonpQueue.call(
    "/login",
    {
      'username': $("#id_uid").val(),
      'password': $("#id_password").val(),
      'back_url': backUrl,
    },
    loginSuccess
  );
  $(this).dialog('close');
}

function loginSuccess(data) {
  if (data.action.cmd == "redirect") {
    location = data.action.data.to_url;
  }
}

function loginError() {
}

function logout() {
  JsonpQueue.call(
    "/logout",
    {},
    function(data) {
      location.reload();
    }
  );
//  showDetailPanel();
}

var panelOn = false;
var detailTitle = null;

function showDetailPanel() {
  if (!panelOn) {
    $("#detail_panel").show("slide", {}, 1000);
    panelOn = true;
  }
}

function hideDetailPanel(onDone) {
  if (panelOn) {
    $("#detail_panel").hide("slide", {}, 1000, onDone)
    panelOn = false;
  }
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
