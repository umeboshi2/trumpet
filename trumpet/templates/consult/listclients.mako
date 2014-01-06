<div class="clients-list">
  <div class="clients-list-header">
    Current Clients
  </div>
  <div class="clients-list-list">
    %for client in clients:
    <div class="clients-list-entry">
      <div class="clients-list-entry-content">
	<% c = client %>
	<% a = '%s' % c.name %>
	<% r = 'consult_clients' %>
	<% kw = dict(context='viewclient', id=c.id) %>
	<% url = request.route_url(r, **kw) %>
	<% kw = dict(context='editclient', id=c.id) %>
	<% edurl = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp<a href="${edurl}">(edit)</a>
      </div>
    </div>
    %endfor
  </div>
</div>
