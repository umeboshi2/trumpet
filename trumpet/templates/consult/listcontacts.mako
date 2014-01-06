<div class="contacts-listusers">
  <div class="contacts-listusers-header">
    Current Contacts
  </div>
  <div class="contacts-listusers-alphamenu">
    %for l in letters:
        <% kw = dict(context='contactlist', id=l) %>
        <% url = request.route_url('consult_frag', **kw) %>
        <div class="action-button letterid" id="${l}">${l}</div>
    %endfor
    <% kw = dict(context='contactlist', id='ALL') %>
    <% url = request.route_url('consult_frag', **kw) %>
    <div class="action-button letterid" id="ALL">All</div>
  </div>
  <div class="contacts-listusers-list">
  </div>
</div>
