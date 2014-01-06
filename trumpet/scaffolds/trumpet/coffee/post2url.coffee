# http://stackoverflow.com/questions/133925/\
# javascript-post-request-like-a-form-submit
window.post_to_url = (path, params, method) ->
        method = method || 'post'
        form = document.createElement('form')
        form.setAttribute('method', method)
        form.setAttribute('action', path)
        for key of params
                if params.hasOwnProperty(key)
                        hiddenField = document.createElement('input')
                        #hiddenField.setAttribute('type', 'text')
                        hiddenField.setAttribute('type', 'hidden')
                        hiddenField.setAttribute('name', key)
                        hiddenField.setAttribute('value', params[key])
                        form.appendChild(hiddenField)
        document.body.appendChild(form)
        form.submit()
                        
                        