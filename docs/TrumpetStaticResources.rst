Trumpet Static Resources
------------------------

CSS Framework
~~~~~~~~~~~~~

-  | `Compass <http://compass-style.org/>`__:
   | Compass is the tool I use to generate my CSS resources. The CSS
     specification has no definitios for variables, forcing many web
     developers to make class names such as "green" and then add CSS
     code like this:

   ::

       .green {
       background-color: green;
       }

But what the developer really needs is something more along this idea:

::

        .warn {
        background-color: $warning-background;
        }
           

. . . which helps to simplify the structure of the CSS and remove some
of the bad hacks that are used to workaround the deficiencies of the CSS
specification.

-  `Susy <http://susy.oddbird.net/>`__\ (Unused): Susy is a grid layout
   system that will allow for responsive webpages. I am not using this
   anymore, as bootstrap is currently handling the responsive grid
   layout, but Susy is superior to bootstrap and since I am also using
   bootstrap-sass, I feel that I can eventually reimplement the
   bootstrap grid layout in Susy. UPDATE: I decided to use the bootstrap
   grid system for the time being.

-  `Sassy Buttons <http://jaredhardy.com/sassy-buttons/>`__: This is a
   collection of mixins and defaults that help a developer make custom
   buttons very easily.

-  `Bootstrap for
   Sass <https://github.com/thomas-mcdonald/bootstrap-sass>`__: This
   wonderful package allows me to refrain from using the css that is
   provided with bootstrap and quickly make a custom version that I can
   integrate more closely with other objects on the page. Having
   bootstrap in this form allows me to adjust how bootstrap operates and
   allows me to only choose the parts I need (Currently everything is
   included).

-  `FontAwesome <http://fontawesome.io/>`__: Instead of just using the
   basic css, I have chosen to use the fontawesome-sass distribution.
   This provides scalable vector icons to websites.

-  `Compass UI <https://github.com/patrickward/compass-ui>`__: This
   compass plugin provides the ability to generate jQueryUI themes with
   a minimum of effort. I have spent hours on the themeroller before
   trying to create a custom theme that would match the general colors
   that I use on a web page. With this plugin, all I have to do is set
   the variables to correspond to the color variables that I use
   elsewhere on the page and I instantly get themed widgets that don't
   look like they came from another site.

Basic Javascript Libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Requirejs <http://requirejs.org>`__: Required.

-  `jQuery <http://jquery.com/>`__: jQuery is a very good for selecting
   and maninpulating elements in the DOM.

-  `jQuery User Interface <http://jqueryui.com/>`__: jQueryUI is used
   for the fullcalendar widget, as well as for dialog boxes and other
   user interface elements that aren't used through boostrap. The
   corresponding styles are maintained with compass.

-  `Bootstrap v3 <http://getbootstrap.com/>`__: Bootstrap is a
   CSS/Javascript framework used to help make responsive websites.
   Bootstrap was selected to be used in order to serve to mobile
   devices. The CSS is handled through compass with bootstrap-sass.

-  `Underscore.js <http://underscorejs.org/>`__: Underscore is a library
   full of useful utilities, and like jqueryui, is depended upon by
   other javascript libraries I use.

-  `Backbone.js <http://backbonejs.org/>`__: Backbone is an excellent
   library that provides an api to make very rich views tied to models
   that are seamlessly synchronized with the server via a REST
   interface.

-  `FullCalendar <http://arshaw.com/fullcalendar/>`__: FullCalendar is a
   very good library that provides an interactive calendar where events
   can be retrieved dynamically and grouped, colored, or otherwised
   styled in many ways. The calendar provides monthly, weekly, and daily
   view models to interact with.

-  `Ace Editor <http://ace.c9.io/#nav=about>`__: The ACE editor is a
   good text editor that is very useful for editing html, css,
   java/coffee scripts, and other formats that aren't being used yet.

-  `CoffeeScript <http://coffeescript.org/>`__: I am currently
   experimenting executing coffeescript on the client using the browser
   to compile the code. While compilation is generally quick on the
   browser, the size of the compiler (196KB, and already minified)
   encourages me to consider implementing server side compilation.

-  `Teacup <http://goodeggs.github.io/teacup/>`__: "Teacup is templates
   in CoffeeScript." -- nuff said
   http://en.wikipedia.org/wiki/Domain-specific\_language

