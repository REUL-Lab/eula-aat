import Controller from '@ember/controller';
import { computed } from '@ember/object';

export default Controller.extend({
    heuristic: computed('model', 'heuristicID', function() {
        const heuristicID = this.get('heuristicID');
        return this.get('model.heuristics').find(function(item) {
            const id = item.name.toLowerCase().replace(/\s/g, '-');
            return heuristicID === id;
        })
    })
});
