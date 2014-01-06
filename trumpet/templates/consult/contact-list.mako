<table>
%for contact in contacts:
    <div class="contacts-listusers-entry">
      <tr>
	<div class="contacts-listusers-entry-content">
	  <% c = contact %>
	  %if c.firstname is not None:
	      <% a = '%s %s' % (c.firstname, c.lastname) %>
	  %elif c.lastname is not None:
              <% a = c.lastname %>
	  %else:
	      <% a = c.email %>
	  %endif
	  <% r = 'consult_contacts' %>
	  <% kw = dict(context='viewcontact', id=c.id) %>
	  <% url = request.route_url(r, **kw) %>
	  %if c.phone:
	      <td class="action-button">
		<strong><a href="tel:${c.phone}">CALL</a></strong>&nbsp;&nbsp;
	      </td>
	  %else:
	      <td></td>
	  %endif
	  <td>
	    <a href="${url}">${a}</a>
	  </td>
	</div>
      </tr>
    </div>
%endfor
</table>
