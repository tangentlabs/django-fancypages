module.exports = function(grunt) {

    var staticPath = function (path) {
        return 'fancypages/static/fancypages/' + path;
    };

    var lessFiles = function (files) {
        var mapping = {};

        for (var idx in files) {
            mapping[file[idx][0]] = file[idx][1];
        };
        return mapping;
    };

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        less: {
            dev: {
                options: {
                    sourceMap: true,
                },
                files: {
                    "fancypages/static/fancypages/dist/css/assets.css": "fancypages/static/fancypages/src/less/assets.less",
                    "fancypages/static/fancypages/dist/css/fancypages.css": "fancypages/static/fancypages/src/less/fancypages.less",
                    "fancypages/static/fancypages/dist/css/page.css": "fancypages/static/fancypages/src/less/page.less",
                    "fancypages/static/fancypages/dist/css/page-management.css": "fancypages/static/fancypages/src/less/page-management.less",
                }
            }
        },

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
    grunt.loadNpmTasks('grunt-contrib-less');

    grunt.registerTask('test', ['mocha']);
    grunt.registerTask('default', ['less:dev']);
};
