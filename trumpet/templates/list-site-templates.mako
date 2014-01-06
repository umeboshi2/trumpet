<div class="list-site-templates-view">
  <% dtformat = '%b %d %Y - %H:%M:%S' %>
  <% timeformat = '%I:%M %p' %>
  <div class="listview-header">
    Site Templates
  </div>
  <div class="listview-list">
    <% route = 'admin_site_templates' %>
    <% ctxt = 'editentry' %>
    <% mkurl = request.route_url %>
    %for t in templates:
    <% url = mkurl(route, context=ctxt, id=t.id) %>
    <div class="listview-list-entry">
      <a href="${url}">${t.name}</a>
    </div>
    %endfor
  </div>
</div>

