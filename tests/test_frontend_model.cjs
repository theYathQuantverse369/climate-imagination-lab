const assert = require('node:assert/strict');
const fs = require('node:fs');
const model = require('../frontend/model.js');

const base = { city: 'Chennai', warming: 3, rainfall: 100, year: 2050, adaptation: 'none', investment: 65 };
const selected = model.calculate(base);
const atThree = Object.fromEntries(Object.entries(selected.curve).map(([key, points]) => [
  key,
  points.find(point => point.warming === 3).risk,
]));

assert.equal(selected.risks['Flood exposure'], 46);
assert.equal(atThree.flood_invested, 46);
assert.ok(atThree.flood_unmitigated >= 60);
assert.ok(atThree.temperature >= 60);
assert.ok(selected.curve.temperature.find(point => point.warming === 2).risk >= 60, 'temperature enters high risk before +3°C');
assert.ok(atThree.temperature - selected.curve.temperature[0].risk > atThree.flood_unmitigated - selected.curve.flood_unmitigated[0].risk, 'temperature climbs fastest');
assert.ok(atThree.people_affected >= 55 && atThree.people_affected <= 60);
assert.ok(model.calculate({ ...base, investment: 0 }).risks['Flood exposure'] > selected.risks['Flood exposure']);
assert.ok(model.calculate({ ...base, rainfall: 130 }).risks['Flood exposure'] > selected.risks['Flood exposure']);
assert.ok(model.calculate({ ...base, year: 2090 }).risks['Heat stress'] > model.calculate({ ...base, year: 2030 }).risks['Heat stress']);
assert.equal(selected.curve.temperature.length, 9);
assert.throws(() => model.calculate({ ...base, investment: 101 }), /between 0 and 100/);

const html = fs.readFileSync(require.resolve('../frontend/index.html'), 'utf8');
const app = fs.readFileSync(require.resolve('../frontend/app.js'), 'utf8');
const htmlIds = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map(match => match[1]));
const directIds = [...app.matchAll(/\$\(['"]#([\w-]+)['"]\)/g)].map(match => match[1]);
assert.deepEqual([...new Set(directIds)].filter(id => !htmlIds.has(id)), [], 'every direct selector must exist in index.html');

console.log('Frontend checks passed: scenarios update, Chennai’s +3°C example matches, and all page selectors exist.');

