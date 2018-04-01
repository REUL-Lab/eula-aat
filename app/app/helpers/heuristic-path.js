import { helper } from '@ember/component/helper';

export function heuristicPath([name]) {
    const id = name.toLowerCase().replace(/\s/g, '-')
    return `analysis.${id}`;
}

export default helper(heuristicPath);
