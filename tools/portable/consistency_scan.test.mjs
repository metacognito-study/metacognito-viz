import test from 'node:test';
import assert from 'node:assert';
import { scanConsistency } from './consistency_scan.mjs';

test('consistent definitions - no conflict', () => {
  const items = [
    { id: '1', text: 'Demand is the quantity of a good that consumers are willing to buy. It decreases as price increases.' },
    { id: '2', text: 'Demand refers to the quantity of a good consumers want to buy at various prices.' },
    { id: '3', text: 'In economics, demand means the quantity of a good consumers are ready to buy.' }
  ];
  
  const result = scanConsistency(items, ['demand']);
  assert.strictEqual(result.meta.terms_scanned, 1);
  assert.strictEqual(result.conflicts.length, 0);
});

test('antonym mismatch conflict', () => {
  const items = [
    { id: '1', text: 'An increase in income means the demand curve shifts to the right.' },
    { id: '2', text: 'An increase in income means the demand curve shifts to the left.' }
  ];
  
  const result = scanConsistency(items, ['increase in income']);
  assert.strictEqual(result.conflicts.length, 1);
  assert.ok(result.conflicts[0].reason.includes("Antonym mismatch ('left' vs 'right')"));
});

test('low overlap conflict', () => {
  const items = [
    { id: '1', text: 'Inflation is a general increase in prices and fall in the purchasing value of money.' },
    { id: '2', text: 'Inflation is defined as the magical process where cats start barking at the moon.' } // Completely different content words
  ];
  
  const result = scanConsistency(items, ['inflation']);
  assert.strictEqual(result.conflicts.length, 1);
  assert.ok(result.conflicts[0].reason.includes("Low lexical overlap"));
});

test('numeric mismatch conflict', () => {
  const items = [
    { id: '1', text: 'The speed of light is defined as 299792 km/s.' },
    { id: '2', text: 'The speed of light is defined as 300000 km/s in some contexts.' }
  ];
  
  const result = scanConsistency(items, ['speed of light']);
  assert.strictEqual(result.conflicts.length, 1);
  assert.ok(result.conflicts[0].reason.includes("Numeric mismatch"));
});

test('negation conflict', () => {
  const items = [
    { id: '1', text: 'Elasticity means demand can respond significantly to price.' },
    { id: '2', text: 'Elasticity means demand can not respond significantly to price.' }
  ];
  
  const result = scanConsistency(items, ['elasticity']);
  assert.strictEqual(result.conflicts.length, 1);
  assert.ok(result.conflicts[0].reason.includes("Negation mismatch"));
});
