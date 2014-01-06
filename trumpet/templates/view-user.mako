<div class="view-user">
  <div class="view-user-header">
    <p>User:  ${user.username}</p>
  </div>
  <div class="view-user-group-list">
    Current Groups
    %for group in user.get_groups():
    <div class="group-list-entry">
      ${group}
    </div>
    %endfor
  </div>
  <div id="adduser-to-group-form">
    ${form|n}
  </div>
</div>
