import config from '../config/environment';
import Ember from 'ember';

export default Ember.Route.extend({
    ajax: Ember.inject.service(),
    model(params) {
        const reqString = `http://${config.APP.apiDomain}/api/results/${params.analysis_id}`;
        const request = this.get('ajax').request(reqString);

        return request.then((result) => {
            let heuristics = [];

            for (let category in result.categories) {
                const heuristicsToAdd = result.categories[category].heuristics;
                heuristics = heuristics.concat(heuristicsToAdd);
            }

            return {
                heuristics: heuristics.sortBy('grade'),
                overallGrade: result.overall_grade,
                title: result.title
            };
        })
    }
});
