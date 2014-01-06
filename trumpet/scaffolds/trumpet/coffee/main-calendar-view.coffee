$(document).ready ->
                
        mouse_over_event = (event, jsEvent, view) ->
                #$('header > h2').text(event.title)
                #$(this).css().clear()
                #content = $(this).html()
                $('header > h2').text(event.title)
                
        loading_events = (bool) ->
                if bool
                        $('#loading').show()
                        $('.fc-header').hide()
                else
                        $('#loading').hide()
                        $('.fc-header').show()

        render_cal_event = (calEvent, element) ->
                element.css
                        'font-size': '0.7em'
                        'padding': '0.2em'
        eventless = () ->
                alert('No events displayed')
                

        evurl = $('#event-source-url').val()
        $('#maincalendar').fullCalendar
                header:
                        left: 'month, agendaWeek, agendaDay'
                        center: 'title'
                theme: true
                eventSources:
                        [
                                url: evurl
                        ]
                editable: false
                droppable: false
                selectable: false
                allDayDefault: false
                loading: loading_events
                eventAfterRender: render_cal_event
                eventRender: render_cal_event
                #eventMouseover: mouse_over_event
                eventColor: '#576B6B'
                defaultView: 'month'
                