<div class="contacts-viewcontact">
  <div class="contacts-viewcontact-header">
    View Contact
  </div>
  <div class="contacts-viewcontact-layout">
    <div class="contacts-viewcontact-content">
      <% a = '%s %s' % (c.firstname, c.lastname) %>
      <% r = 'consult_contacts' %>
      <% kw = dict(context='viewcontact', id=c.id) %>
      <% url = request.route_url(r, **kw) %>
      <% kw = dict(context='editcontact', id=c.id) %>
      <% edurl = request.route_url(r, **kw) %>
      <% kw = dict(context='exportcontact', id=c.id) %>
      <% exurl = request.route_url(r, **kw) %>
      <% kw = dict(context='delete', id=c.id) %>
      <% delurl = request.route_url(r, **kw) %>
      ${a}<br>
      Phone: ${c.phone}
      %if c.phone:
          <strong><a href="tel:${c.phone}">CALL</a></strong>&nbsp;&nbsp;
      %endif
      <br>
      Email: ${c.email}<br>
      <a href="${edurl}">(edit)</a>
      <a href="${exurl}">(export)</a>
      <a href="${delurl}">(delete)</a>
    </div>
  </div>
  <hr>
  <div>
    <% kw = dict(context='list', id='all') %>
    <% lsurl = request.route_url(r, **kw) %>
    <a href="${lsurl}">List Contacts</a>
  </div>
</div>
