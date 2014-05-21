module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    mocha: {
        test: {                                                                                                                                                                                                                                                           
            options: {                                                                                                                                                                                                                                                    
                reporter: 'Spec'                                                                                                                                                                                                                                          
            },                                                                                                                                                                                                                                                            
            src: ['tests/javascript/**/*.html'],                                                                                                                                                                                                                          
        },                                                                                                                                                                                                                                                                
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-mocha');

  // Default task(s).
  grunt.registerTask('test', ['mocha']);

};
