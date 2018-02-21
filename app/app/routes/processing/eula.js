import Ember from 'ember';

export default Ember.Route.extend({
  afterModel() {
    setTimeout(() => {
      this.transitionTo('analysis');
    }, 2500);
  }
});
