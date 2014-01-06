<div class="admin-show-site-path-content-view">
  <% dtformat = '%b %d %Y - %H:%M:%S' %>
  <% timeformat = '%I:%M %p' %>
  <% route = 'admin_sitecontent_mgr' %>
  <% mkurl = request.route_url %>
  <div class="listview-header">
    Site Content for ${path.name}
  </div>
  <div class="listview-list">
    <div class="listview-list-entry-header">
      CSS Resources
    </div>
    <% route = 'admin_sitecontent_mgr' %>
    <% ctxt = 'showcss' %>
    %for obj in csslist:
    <% url = mkurl(route, context=ctxt, id=obj.css_id) %>
    <div class="listview-list-entry">
      <a href="${url}">${obj.css.name}</a>
      <% detach_id = 'css-%d-%d' % (path.id, obj.css_id) %>
      <% detach_url = mkurl(route, context='detach', id=detach_id) %>
      <div class="action-button detach-button" id="detach-${detach_id}" href="${detach_url}">
	detach
      </div>
    </div>
    %endfor
    <% attach_url = mkurl(route, context='attachcss', id=path.id) %>
    <div class="action-button" id="attach-css-button" href="${attach_url}">
      Attach CSS
    </div>
  </div>
  <div class="listview-list">
    <div class="listview-list-entry-header">
      JS Resources
    </div>
    <% route = 'admin_sitecontent_mgr' %>
    <% ctxt = 'showjs' %>
    %for obj in jslist:
    <% url = mkurl(route, context=ctxt, id=obj.js_id) %>
    <div class="listview-list-entry">
      <a href="${url}">${obj.js.name}</a>
      <% detach_id = 'js-%d-%d' % (path.id, obj.js_id) %>
      <% detach_url = mkurl(route, context='detach', id=detach_id) %>
      <div class="action-button detach-button" id="detach-${detach_id}" href="${detach_url}">
	detach
      </div>
    </div>
    %endfor
    <% attach_url = mkurl(route, context='attachjs', id=path.id) %>
    <div class="action-button" id="attach-js-button" href="${attach_url}">
      Attach JS
    </div>
  </div>
</div>

