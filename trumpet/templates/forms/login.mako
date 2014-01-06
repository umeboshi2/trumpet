<div class="loginmessage">
${message}
</div>
<form action="${action}" method="post">
<div>${form.came_from(value=came_from)}</div>
<div>
<table>
<tr>
<td><div>${form.login.label()}</td><td>${form.login()}</div></td>
</tr>
<tr>
<td><div>${form.password.label()}</td><td>${form.password()}</div></td>
</tr>
<tr>
<td><div>${form.submit.label()}</td><td>${form.submit()}</div></td>
</tr>
</table>
</div>
</form>
