<div class="admin-list-site-paths-view">
  <% dtformat = '%b %d %Y - %H:%M:%S' %>
  <% timeformat = '%I:%M %p' %>
  <div class="listview-header">
    Site Paths
  </div>
  <div class="listview-list">
    <% route = 'admin_sitecontent_mgr' %>
    <% ctxt = 'showcontent' %>
    <% mkurl = request.route_url %>
    %for p in paths:
    <% url = mkurl(route, context=ctxt, id=p.id) %>
    <div class="listview-list-entry">
      <a href="${url}">${p.name}</a>
      %if p.css:
      <span>(CSS)</span>
      %endif
      %if p.js:
      <span>(JS)</span>
      %endif
      <div class="action-button delete-button" id="delete-path-${p.id}">Delete</div>
    </div>
    %endfor
  </div>
</div>

