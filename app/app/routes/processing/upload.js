import Ember from 'ember';

export default Ember.Route.extend({
  afterModel() {
    setTimeout(() => {
      this.transitionTo('processing.download');
    }, 2500);
  }
});
