<%
# run the python here
import os, sys
if 'EDITOR' in os.environ:
  editor = os.environ['EDITOR']
else:
  editor = 'something else'
cntext = request.matchdict['context']
if ctype == 'css':
  title = "Site CSS Resources"
  show_ctxt = 'showcss'
elif ctype == 'js':
  title = "Site Javascript Resources"
  show_ctxt = 'showjs'
else:
  raise RuntimeError, "Bad ctype %s" % ctype
%>
<div class="admin-list-site-${ctype}-view">
  <input type="hidden" id="ctype" value="${ctype}">
  <% dtformat = '%b %d %Y - %H:%M:%S' %>
  <% timeformat = '%I:%M %p' %>
  <div class="listview-header">
    ${title}
  </div>
  <div class="listview-list">
    <% route = 'admin_sitecontent_mgr' %>
    <% ctxt = show_ctxt %>
    <% mkurl = request.route_url %>
    %for r in rlist:
    <% url = mkurl(route, context=ctxt, id=r.id) %>
    <div class="listview-list-entry" id="entry-${ctype}-${r.id}">
      <a href="${url}">${r.name}</a>
      <div class="action-button delete-button" id="delete-${ctype}-${r.id}">
	Delete
      </div>
      <div class="delete-confirm" id="div-confirm-${ctype}-${r.id}">
	<strong>Confirm Deletion</strong>
	<div class="action-button confirm-button" id="confirm-${ctype}-${r.id}">
	  Confirm
	</div>
	<div class="action-button cancel-button" id="cancel-${ctype}-${r.id}">
	  Cancel
	</div>
	
      </div>
    </div>
    %endfor
  </div>
</div>

