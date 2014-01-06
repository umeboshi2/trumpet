<!doctype html>
<!--[if lt IE 7]><html class="no-js ie6" lang="en"><![endif]-->
<!--[if IE 7]><html class="no-js ie7" lang="en"><![endif]-->
<!--[if IE 8]><html class="no-js ie8" lang="en"><![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" dir="ltr" lang="en-US"><!--<![endif]-->
<head>
  <title>${layout.title}</title>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
  <body>
    <div class="page">
      <div id="top-bar">
	<div class="horizontal-menu">
	  ${layout.main_menu|n}
	</div>
	<header class="header">
	  <h1>${layout.header}</h1>
	  <h2>${layout.subheader}</h2>
	</header>
      </div>
      <div class="sidebar">
	${unicode(layout.ctx_menu)|n}
	% if 'user' in request.session and request.session['user']:
	<a id="sidebar-logout" href="${request.application_url}/logout">Logout ${request.session['user'].username}</a>
	% endif
	<div class="widgetbox">
	  ${layout.widgetbox|n}
	</div>
      </div>
      <div class="content">
	${layout.content|n}
      </div>
      <div class="footer">
	${layout.footer|n}
      </div>
    </div>
  </body>
</html>
