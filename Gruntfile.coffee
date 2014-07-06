# Gruntfile for sitecontent

module.exports = (grunt) ->
  # variables to use in config
  # foo = 'bar'
  app_dir = 'trumpet/static'
    
  # config
  grunt.initConfig
    coffee:
      compile:
        options:
          bare: false
        expand: true
        src: ['apps/**/*.coffee']
        dest: app_dir
        ext: '.js'
                
      compileWithMaps:
        options:
          bare: false
          sourceMap: true
        expand: true
        src: ['apps/**/*.coffee']
        dest: app_dir
        ext: '.js'
                
    compass:
      compile:
        config: 'config.rb'
        
    watch:
      coffee:
        files: ['apps/**/*.coffee']
        tasks: ['coffee:compileWithMaps']
      compass:
        files: ['sass/**/*.scss']
        tasks: ['compass']
      cpcoffee:
        files: ['apps/**/*.coffee']
        tasks: ['copy:coffee']
        
    copy:
      coffee:
        files:
          [
            expand: true
            src: ['apps/**']
            dest: 'trumpet/static/'
          ]  
        
        
    clean:
      js:
        src: ['trumpet/static/apps/**/*.js']
      emacs:
        src: ['**/*~']
        
    shell:
      scss:
        command: 'python scripts/generate-scss.py'
      googlefonts:
        command: 'python scripts/get-google-fonts.py'
        options:
          stdout: true
      bower:
        command: 'python scripts/prepare-bower-components.py'
        options:
          stdout: true
        
    # load grunt-* tasks
    require('matchdep').filterDev('grunt-*').forEach grunt.loadNpmTasks
    
    grunt.registerTask 'default', [
      'shell:scss'
      'shell:bower'
      'coffee:compile'
      'compass:compile'
      ]
                          
        