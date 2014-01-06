// Generated by CoffeeScript 1.6.1
(function() {

  $(document).ready(function() {
    var ctype, editor, fresh_edit;
    $('#save-content').hide();
    ctype = $('#ctype').val();
    fresh_edit = function(data, status, xhr) {
      return $('#save-content').hide();
    };
    editor = ace.edit('editor');
    editor.getSession().on('change', function() {
      return $('#save-content').show();
    });
    if (ctype === 'css') {
      editor.getSession().setMode('ace/mode/css');
    }
    if (ctype === 'js') {
      editor.getSession().setMode('ace/mode/javascript');
    }
    editor.setTheme('ace/theme/twilight');
    return $('#save-content').click(function() {
      var formdata;
      formdata = {
        update: 'submit',
        content: editor.getValue()
      };
      $(this).hide();
      return $.post(window.location, formdata, fresh_edit);
    });
  });

}).call(this);
