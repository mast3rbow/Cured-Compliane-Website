var gulp = require('gulp'),
    postcss = require('gulp-postcss'),
    concatCss = require('gulp-concat-css');

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
      .pipe(concatCss('page.css'))
      .pipe(gulp.dest('static/css/'));
  });