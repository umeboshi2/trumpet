# Gruntfile for sitecontent

module.exports = (grunt) ->
  # variables to use in config
  # foo = 'bar'
  app_dir = 'javascripts'
    
  # config
  grunt.initConfig
    coffee:
      compile:
        options:
          bare: false
        expand: true
        src: ['**/*.coffee']
        dest: app_dir
        ext: '.js'
        cwd: 'coffee'
                
      compileWithMaps:
        options:
          bare: false
          sourceMap: true
        expand: true
        src: ['**/*.coffee']
        dest: app_dir
        ext: '.js'
        cwd: 'coffee'
                
    compass:
      compile:
        config: 'config.rb'
        
    watch:
      coffee:
        files: ['coffee/**/*.coffee']
        tasks: ['coffee:compileWithMaps', 'copy:coffee']
      compass:
        files: ['sass/**/*.scss']
        tasks: ['compass']
        
    copy:
      coffee:
        files:
          [
            expand: true
            src: ['**/*.coffee']
            dest: app_dir
            cwd: 'coffee'
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
                          
        