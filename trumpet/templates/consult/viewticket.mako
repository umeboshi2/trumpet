<div class="ticket-view">
  <div class="ticket-header">
    ${ticket.title}
  </div>
  <div class="ticket-description">
    ${rst(ticket.description)|n}
  </div>
  <div class="ticket-history">
    %for tstatus in ticket.history:
    <div class="ticket-status-entry">
      <div class="ticket-status-entry-content">
	<% c = tstatus %>
	<div class="ticket-status-entry-changedate">
	  <% format = '%a %H:%M       -----       %d %B, %Y' %>
	  ${c.changed.strftime(format)}
	</div>
	<% status = tm.stypes.get(c.status).name %>
	<% msg = '%s(%s)' % (status, str(c.user)) %>
	<div class="ticket-status-entry-changed">
	  ${msg}
	</div>
	<div class="ticket-status-entry-reason">
	  ${rst(c.reason)|n}
	</div>
      </div>
    </div>
    %endfor
  </div>
  <div class="ticket-update-ticket">
    <% kw = dict(context='updateticket', id=ticket.id) %>
    <% url = request.route_url('consult_tickets', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
