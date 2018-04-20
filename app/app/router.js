import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('home', { path: '/' });
  this.route('analysis', {path: '/analysis/:analysis_id'}, function() {
    this.route('document-length');
    this.route('ease-of-navigation');
    this.route('mobile-accessibility');
    this.route('mobile-readability');
    this.route('notify-changes-in-policy');
    this.route('plain-language');
    this.route('type-conventions');
  });
  this.route('processing', function() {
    this.route('download');
    this.route('eula');
    this.route('pdf');
  });
});

export default Router;
