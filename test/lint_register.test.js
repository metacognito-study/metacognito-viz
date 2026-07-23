const assert = require('assert');
const path = require('path');
const { lintBook } = require('../scripts/lint_register.js');

function runTests() {
    let failed = false;
    const fixturesDir = path.join(__dirname, 'fixtures');

    // Test 1: Passing text (all rules)
    const passingRes = lintBook(path.join(fixturesDir, 'passing.json'));
    try {
        assert.strictEqual(passingRes.errors.length, 0, 'Passing file should have 0 errors');
        console.log('✅ test/fixtures/passing.json passed');
    } catch (e) {
        console.error('❌ test/fixtures/passing.json failed:', e.message);
        failed = true;
    }

    // Test 2: Failing file with all errors
    const failingRes = lintBook(path.join(fixturesDir, 'failing.json'));
    try {
        assert.ok(failingRes.errors.some(e => e.type === 'TASHKEEL_COVERAGE'), 'Should detect bare word');
        assert.ok(failingRes.errors.some(e => e.type === 'GRADE_LIMITS'), 'Should detect grade limits violation');
        assert.ok(failingRes.errors.some(e => e.type === 'DIALECT_PLACEMENT'), 'Should detect dialect placement violation');
        assert.ok(failingRes.errors.some(e => e.type === 'DASH_BAN'), 'Should detect dash ban violation');
        assert.ok(failingRes.warnings.some(w => w.type === 'FOREIGN_SAFETY'), 'Should detect foreign/safety keyword');
        console.log('✅ test/fixtures/failing.json tested successfully');
    } catch (e) {
        console.error('❌ test/fixtures/failing.json failed:', e.message);
        failed = true;
    }

    // Test 3: Sentence length limits
    const failingSentenceLengthRes = lintBook(path.join(fixturesDir, 'failing_sentence_length.json'));
    try {
        const gradeErr = failingSentenceLengthRes.errors.find(e => e.type === 'GRADE_LIMITS');
        assert.ok(gradeErr, 'Should detect sentence length violation');
        assert.match(gradeErr.message, /Too many words in sentence/);
        console.log('✅ test/fixtures/failing_sentence_length.json tested successfully');
    } catch (e) {
        console.error('❌ test/fixtures/failing_sentence_length.json failed:', e.message);
        failed = true;
    }

    // Test 4: Passing Dialect
    const passingDialectRes = lintBook(path.join(fixturesDir, 'passing_dialect.json'));
    try {
        assert.strictEqual(passingDialectRes.errors.filter(e => e.type === 'DIALECT_PLACEMENT').length, 0, 'Should not fail dialect inside dialogue');
        console.log('✅ test/fixtures/passing_dialect.json tested successfully');
    } catch (e) {
        console.error('❌ test/fixtures/passing_dialect.json failed:', e.message);
        failed = true;
    }
    
    // Test 5: Failing Dialect
    const failingDialectRes = lintBook(path.join(fixturesDir, 'failing_dialect.json'));
    try {
        assert.ok(failingDialectRes.errors.some(e => e.type === 'DIALECT_PLACEMENT'), 'Should detect dialect in narration');
        console.log('✅ test/fixtures/failing_dialect.json tested successfully');
    } catch (e) {
        console.error('❌ test/fixtures/failing_dialect.json failed:', e.message);
        failed = true;
    }

    if (failed) {
        process.exit(1);
    } else {
        console.log('\nAll tests passed! 🎉');
        process.exit(0);
    }
}

runTests();
