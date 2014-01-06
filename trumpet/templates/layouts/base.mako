<!doctype html>
<!--[if lt IE 7]><html class="no-js ie6" lang="en"><![endif]-->
<!--[if IE 7]><html class="no-js ie7" lang="en"><![endif]-->
<!--[if IE 8]><html class="no-js ie8" lang="en"><![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" dir="ltr" lang="en-US"><!--<![endif]-->
<head>
  <% title = '' %>
  %if layout.title is not None:
  <% title = layout.title %>
  <title>${title}</title>
  %endif
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  ${''.join(layout.css)|n}
  ${''.join(layout.js)|n}
</head>
  <body>
    <div class="page">
      <nav class="main-menu navbar navbar-default navbar-fixed-top" data-spy="affix" data-offset-top="10">
	<div class="navbar-header">
	  <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#ctx-menu-collapse-1">
	    <span class="sr-only">Toggle navigation</span>
	    <span class="badge">expand</span>
	  </button>
	  %if layout.brand is not None:
	  <% brand = layout.brand %>
	  <a class="navbar-brand" href="/">${brand}</a>
	  %endif
	</div>
	<div class="collapse navbar-collapse" id="ctx-menu-collapse-1">
	  %if layout.user_menu is not None:
	  <div class="main-user-menu navbar navbar-nav navbar-right">
	    ${unicode(layout.user_menu)|n}
	  </div>
	  %endif
	  %if layout.options_menus is not None:
	    %for menu in layout.options_menus:
	      <div class="navbar navbar-nav navbar-right">
		${unicode(layout.options_menus[menu])|n}
	      </div>
	    %endfor
	  %endif
	  <% cmenu_test = layout.ctx_menu is not None %>
	  %if cmenu_test:
	  <div class="nav navbar-nav navbar-right">
	    ctxmenu_deprecated${str(cmenu_test)|n}----${str(type(unicode(layout.ctx_menu)))}
	    <!--${unicode(layout.ctx_menu)|n} -->
	  </div>
	  %endif
	  %if layout.main_menu is not None:
	  <ul class="nav navbar-nav navbar-left">
	    <li>
	      ${layout.main_menu.render() |n}
	    </li>
	  </ul>
	  %endif
	</div>
      </nav>
      <div class="main-content">
	  %if layout.header is not None:
	  <div class="header">
	    <% header = '' %>
	    <% header = layout.header %>
	    ${header}
	  </div>
	  %endif
	  %if layout.subheader is not None:
	  <div class="subheader">
	    <% subheader = '' %>
	    <% subheader = layout.subheader %>
	    ${subheader}
	  </div>
	  %endif
	  %if layout.widgetbox is not None:
	  <div class="widgetbox">
	    <% widgetbox = '' %>
	    <% widgetbox = layout.widgetbox %>
	    ${widgetbox|n}
	  </div>
	  %endif
	%if layout.sidebar is None:
	  %if layout.content is not None:
	    <div class="content">
	      ${layout.content|n}
	    </div>
	  %endif
	%else:
	  <div class="two-col">
	    <div class="sidebar">
	      <% sidebar = layout.sidebar %>
	      ${sidebar|n}
	    </div>
	    %if layout.content is not None:
	      <div class="right-column-content">
		${layout.content|n}
	      </div>
	    %endif
	  </div>
	  %endif
	  %if layout.footer is not None:
	  <div class="footer">
	    <% footer = '' %>
	    <% footer = layout.footer %>
	    ${footer|n}
	  </div>
	  %endif
      </div>
      <div class="status-bar navbar navbar-default navbar-fixed-bottom" data-spy="affix" data-offset-bottom="17">
	<div class="status-bar-message"></div>
	<div class="navbar-header">
	  <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#ctx-menu-collapse-2">
	    <span class="sr-only">Toggle navigation</span>
	    <span class="label label-danger">expand</span>
	    <!--<span class="icon-bar"></span>
		<span class="icon-bar"></span>-->
	  </button>
	</div>
	<div class="collapse navbar-collapse" id="ctx-menu-collapse-2">
	  <div class="nav navbar-nav navbar-right">
	  </div>
	  <ul class="nav navbar-nav navbar-left">
	  </ul>
	</div>
      </div>
    </div>
  </body>
</html>
