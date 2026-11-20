var gulp = require('gulp'),
    postcss = require('gulp-postcss');

gulp.task('css', function () {
    return gulp.src('./src/css/page.css')
      .pipe(postcss([
        require('tailwindcss'),
        require('autoprefixer'),
        require('cssnano')({
          preset: ['default', {
            discardComments: { removeAll: true }
          }]
        })
      ]))
      .pipe(gulp.dest('static/css/'));
  });
