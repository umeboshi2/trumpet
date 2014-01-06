<div class="tickets-list">
  <% dtformat = '%D %H:%m' %>
  <table class="site-text-table">
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Created</th>
      <th>Modified</th>
      <th>Edit</th>
    </tr>
    %for entry in entries:
    <% getdata = dict(context='viewentry', id=entry.id) %>
    <% href_view = viewer.url(**getdata) %>
    <% getdata['context'] = 'editentry' %>
    <% href_edit = viewer.url(**getdata) %>
    <tr>
      <td><a href="${href_view}">${entry.name}</a></td>
      <td>${entry.type}</td>
      <td>${entry.created.strftime(dtformat)}</td>
      <td>${entry.modified.strftime(dtformat)}</td>
      <td><a href="${href_edit}">(edit)</a></td>
    </tr>
    %endfor
  </table>
</div>
