<div class="tickets-list">
  <div class="tickets-list-header">
    Current Tickets
  </div>
  <div class="tickets-list-list">
    %for ticket in tickets:
    <div class="tickets-list-entry">
      <div class="tickets-list-entry-content">
	<% c = ticket %>
	<% a = '%s' % c.title %>
	<% r = 'consult_tickets' %>
	<% kw = dict(context='viewticket', id=c.id) %>
	<% url = request.route_url(r, **kw) %>
	<% status = tm.get_status(c.id) %>
	<a href="${url}">${a}</a>
	<div class="tickets-list-entry-status">
	  ${status}
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
