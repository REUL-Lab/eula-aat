import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('home', {path: '/'});
  this.route('analysis');
  this.route('processing', {path: '/processing'}, function() {
    this.route('download');
    this.route('eula');
    this.route('pdf');
  });
});

export default Router;
