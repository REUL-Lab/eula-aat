import Ember from 'ember';

export default Ember.Route.extend({
    ajax: Ember.inject.service(),
    model() {
        const request = this.get('ajax').request('http://127.0.0.1:5000/api/results/5ac02236f5f9e90012b70e3c');

        return request.then((result) => {
            let heuristics = [];

            for (let category in result.categories) {
                const heuristicsToAdd = result.categories[category].heuristics;
                heuristics = heuristics.concat(heuristicsToAdd);
            }

            return heuristics;
        })

        // return [
        //         {
        //             'name' : 'Document Length',
        //             'description' : ["bullet point 1","bullet point 2", "bullet point 3"],
        //             'numwords' : 1909,
        //             "score" : 'A'
        //         },
        //         {
        //             "name" : "Ease of Navigation",
        //             "description" : ["bullet point 1", "bullet point 2", "bullet point 3", "bullet point 4"],
        //             "reason" : "Not implemented",
        //             "score" : "B"
        //         }
        // ]

    }
});
