import Ember from 'ember';

export default Ember.Route.extend({
    ajax: Ember.inject.service(),
    model() {
        const request = this.get('ajax').request('http://127.0.0.1:5000/api/results/5ac046e0f5f9e90452cdf4f8');

        return request.then((result) => {
            let heuristics = [];

            for (let category in result.categories) {
                const heuristicsToAdd = result.categories[category].heuristics;
                heuristics = heuristics.concat(heuristicsToAdd);
            }

            return {
                heuristics: heuristics,
                overallGrade: result.overall_grade
            };
        })
    }
});
