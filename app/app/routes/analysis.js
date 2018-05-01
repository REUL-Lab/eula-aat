import config from '../config/environment';
import Ember from 'ember';

export default Ember.Route.extend({
    ajax: Ember.inject.service(),
    model(params) {
        const reqString = `http://${config.APP.apiDomain}/api/results/${params.analysis_id}`;
        const request = this.get('ajax').request(reqString);

        return request.then((result) => {
            let heuristics = [];
            const classes = ['text-danger', 'text-warning', 'text-success', 'text-info']

            for (let category in result.categories) {
                let heuristicsToAdd = result.categories[category].heuristics;
                heuristicsToAdd.forEach(function(heuristic){
                    heuristic.feedback.forEach(function(fb) {
                        fb.class = classes[fb.rating]
                    });
                });
                heuristics = heuristics.concat(heuristicsToAdd);
            }

            return {
                heuristics: heuristics.sortBy('grade'),
                overallGrade: result.overall_grade,
                title: result.title,
                url: result.url
            };
        })
    }
});
