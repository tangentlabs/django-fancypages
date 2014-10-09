module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        less: {
            dist: {
                options: {
                    cleancss: true,
                    compress: true,
                },
                files: {
                    "fancypages/static/fancypages/dist/css/fp-assets.min.css": "fancypages/static/fancypages/src/less/fp-assets.less",
                    "fancypages/static/fancypages/dist/css/fp-editor.min.css": "fancypages/static/fancypages/src/less/fp-editor.less",
                    "fancypages/static/fancypages/dist/css/fp-dashboard.min.css": "fancypages/static/fancypages/src/less/fp-dashboard.less",
                    "fancypages/static/fancypages/dist/css/fancypages.min.css": "fancypages/static/fancypages/src/less/fancypages.less",
                }
            },
        },

        cssmin: {
            dist: {
                files: {
                    "fancypages/static/fancypages/dist/css/libs.min.css": [
                        "fancypages/static/fancypages/src/libs/jquery.flexslider/flexslider.css",
                        "fancypages/static/fancypages/src/libs/rangeslider/rangeslider.css",
                    ],
                    "fancypages/static/fancypages/dist/libs/rangeslider/rangeslider.min.css": [
                        "fancypages/static/fancypages/src/libs/rangeslider/rangeslider.css"
                    ]
                }
            }
        },

        uglify: {
            dist: {
                files: {
                    "fancypages/static/fancypages/dist/js/libs.min.js": [
                        "fancypages/static/fancypages/src/js/jquery-sortable.js"
                    ],
                    "fancypages/static/fancypages/dist/libs/rangeslider/rangeslider.min.js": [
                        "fancypages/static/fancypages/src/libs/rangeslider/rangeslider.min.js"
                    ],
                    "fancypages/static/fancypages/dist/js/fancypages.min.js": [
                        "fancypages/static/fancypages/src/js/app.js",
                        "fancypages/static/fancypages/src/js/api.js",
                        "fancypages/static/fancypages/src/js/models.js",
                        "fancypages/static/fancypages/src/js/views.js"
                    ],
                    "fancypages/static/fancypages/dist/js/dashboard.min.js": [
                        "fancypages/static/fancypages/src/js/dashboard/models.js",
                        "fancypages/static/fancypages/src/js/dashboard/views.js"
                    ],
                }
            },
        },

        mocha: {
            test: {
                options: {
                    reporter: 'Spec'
                },
                src: ['tests/javascript/**/*.html'],
            },
        },

        watch: {
            options: {
                livereload: true,
                atBegin: true
            },
            javascript: {
                files: [
                    'fancypages/static/fancypages/src/js/**/*.js',
                    'fancypages/templates/**/*.jst',
                    'fancypages/templates/**/*.html',
                ],
                tasks: ['uglify']
            },
            styles: {
                files: [
                    'fancypages/static/fancypages/src/less/**/*.less',
                    'fancypages/templates/**/*.html',
                ],
                tasks: ['less', 'cssmin']
            }
        }
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-mocha');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');

    grunt.registerTask('test', ['mocha']);
    grunt.registerTask('default', ['less', 'cssmin', 'uglify']);
};
