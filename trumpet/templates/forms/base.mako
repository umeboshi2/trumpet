<form action="${action}" method="post">
<div>
<table>
%for field in form:
    <tr>
        <td><div>${field.label}:</td>
        <td>${field()}</div></td>
    </tr>
%endfor
<tr>
<td><div>${form.submit.label}:</td><td>${form.submit()}</div></td>
</tr>
</table>
</div>
</form>
