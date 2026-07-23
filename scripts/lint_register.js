#!/usr/bin/env node

/**
 * Dependency-free Node linter that mechanically enforces the Fushia v2
 * register and leveling rules on any book JSON in public/assets/stories/
 */

const fs = require('fs');
const path = require('path');

// --- Rules Configurations ---

// Arabic Diacritics Range
const TASHKEEL_REGEX_GLOBAL = /[\u064B-\u0653]/g;
const TASHKEEL_REGEX = /[\u064B-\u0653]/;

// Dash Regex
const DASH_REGEX = /[–—]/g; // en-dash, em-dash

// Dialect defaults
let DIALECT_WORDS = ['يبغى', 'حلو', 'مرة', 'الحين'];
const LEXICON_PATH = path.join(__dirname, 'white_fusha_lexicon.json');
try {
  if (fs.existsSync(LEXICON_PATH)) {
    const lexicon = JSON.parse(fs.readFileSync(LEXICON_PATH, 'utf8'));
    if (Array.isArray(lexicon)) {
      DIALECT_WORDS = Array.from(new Set([...DIALECT_WORDS, ...lexicon]));
    }
  }
} catch (e) {
  console.warn("Warning: Could not load white_fusha_lexicon.json", e.message);
}

// Safety/Foreign Warnings defaults
const SAFETY_KEYWORDS = [
  'music', 'instrument', 'magic', 'romance', 
  'موسيقى', 'سحر', 'رومانسية', 'حب', 'غرام', 'عشق', 'أغنية', 'اغنية', 'مزمار', 'قيثارة'
];

// Grade Limits
const GRADE_LIMITS = {
  1: { maxWordsPerSentence: 5, maxSentencesPerPage: 2 },
  2: { maxWordsPerSentence: 7, maxSentencesPerPage: null }, 
  3: { maxWordsPerSentence: 10, maxSentencesPerPage: 3 }
};

// --- Helpers ---

// Split text into words (Arabic words for tashkeel, or just space-separated)
function extractWords(text) {
    return text.split(/\s+/).map(w => w.replace(/[.,!؟"«»()[\]{}؛،:–—]/g, '')).filter(w => w.length > 0);
}

// Extract text outside of guillemets
function extractNarration(text) {
    // Replaces everything between « and » (inclusive) with a space
    return text.replace(/«[^»]*»/g, ' ');
}

// Split page text into sentences
function splitSentences(text) {
    // Simple sentence splitter based on Arabic and English end punctuation
    return text.split(/(?<=[.!?؟\n])\s+/).filter(s => s.trim().length > 0);
}

function countWords(text) {
    return text.split(/\s+/).filter(w => w.trim().replace(/[.,!؟"«»()[\]{}؛،:–—]/g, '').length > 0).length;
}

function checkTashkeelCoverage(text, errors, pageIdx) {
    const narration = extractNarration(text);
    const words = narration.split(/\s+/);
    
    let wordIdx = 0;
    words.forEach((word) => {
        const cleanWord = word.replace(/[.,!؟"«»()[\]{}؛،:–—]/g, '');
        if (!cleanWord) return;
        
        const isArabic = /[\u0621-\u064A]/.test(cleanWord);
        if (isArabic) {
            // Report any bare/unvowelled word
            if (!TASHKEEL_REGEX.test(cleanWord)) {
                errors.push({
                    type: 'TASHKEEL_COVERAGE',
                    message: `Bare/unvowelled Arabic word found in narration: "${cleanWord}"`,
                    page: pageIdx,
                    wordIndex: wordIdx
                });
            }
        }
        wordIdx++;
    });
}

function checkGradeLimits(text, grade, errors, pageIdx) {
    const limits = GRADE_LIMITS[grade];
    if (!limits) return;

    const sentences = splitSentences(text);
    
    if (limits.maxSentencesPerPage && sentences.length > limits.maxSentencesPerPage) {
        errors.push({
            type: 'GRADE_LIMITS',
            message: `Too many sentences on page. Grade ${grade} allows max ${limits.maxSentencesPerPage}, found ${sentences.length}.`,
            page: pageIdx
        });
    }

    sentences.forEach((sentence, sentenceIdx) => {
        const wordCount = countWords(sentence);
        if (wordCount > limits.maxWordsPerSentence) {
            errors.push({
                type: 'GRADE_LIMITS',
                message: `Too many words in sentence. Grade ${grade} allows max ${limits.maxWordsPerSentence}, found ${wordCount} in sentence: "${sentence.substring(0, 30)}..."`,
                page: pageIdx,
                sentenceIndex: sentenceIdx
            });
        }
    });
}

function checkDialectPlacement(text, errors, pageIdx) {
    const narration = extractNarration(text);
    const words = extractWords(narration);
    
    words.forEach((word, wordIdx) => {
        const normalizedWord = word.replace(TASHKEEL_REGEX_GLOBAL, '');
        
        if (DIALECT_WORDS.includes(normalizedWord)) {
            errors.push({
                type: 'DIALECT_PLACEMENT',
                message: `Dialect word "${normalizedWord}" found outside dialogue (narration).`,
                page: pageIdx,
                wordIndex: wordIdx
            });
        }
    });
}

function checkDashBan(text, errors, pageIdx) {
    let match;
    while ((match = DASH_REGEX.exec(text)) !== null) {
        errors.push({
            type: 'DASH_BAN',
            message: `Forbidden dash character found: "${match[0]}"`,
            page: pageIdx,
            index: match.index
        });
    }
}

function checkForeignSafety(text, warnings, pageIdx) {
    const lowerText = text.toLowerCase();
    SAFETY_KEYWORDS.forEach(keyword => {
        if (lowerText.includes(keyword.toLowerCase())) {
            warnings.push({
                type: 'FOREIGN_SAFETY',
                message: `Content safety/foreign keyword detected: "${keyword}"`,
                page: pageIdx
            });
        }
    });
}

// --- Main Linter ---

function lintBook(filePath) {
    const results = {
        file: filePath,
        errors: [],
        warnings: []
    };

    let book;
    try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        book = JSON.parse(fileContent);
    } catch (e) {
        results.errors.push({ type: 'PARSE_ERROR', message: `Could not parse JSON: ${e.message}` });
        return results;
    }

    const grade = book.grade || null;
    const pages = book.pages || [];

    if (!Array.isArray(pages)) {
         results.errors.push({ type: 'SCHEMA_ERROR', message: `book.pages must be an array` });
         return results;
    }

    pages.forEach((page, pageIdx) => {
        const text = page.text || "";
        if (!text) return;

        checkTashkeelCoverage(text, results.errors, pageIdx);
        if (grade) {
            checkGradeLimits(text, grade, results.errors, pageIdx);
        }
        checkDialectPlacement(text, results.errors, pageIdx);
        checkDashBan(text, results.errors, pageIdx);
        checkForeignSafety(text, results.warnings, pageIdx);
    });

    return results;
}

// --- CLI Execution ---

function run() {
    const args = process.argv.slice(2);
    const isJsonOutput = args.includes('--json');
    const fileArgs = args.filter(a => a !== '--json');

    let filesToLint = fileArgs;
    if (filesToLint.length === 0) {
        const defaultDir = path.join(process.cwd(), 'public', 'assets', 'stories');
        if (fs.existsSync(defaultDir)) {
            filesToLint = fs.readdirSync(defaultDir)
                .filter(f => f.endsWith('.json'))
                .map(f => path.join(defaultDir, f));
        }
    }

    if (filesToLint.length === 0) {
        if (!isJsonOutput) console.log("No files to lint.");
        process.exit(0);
    }

    const allResults = [];
    let hasErrors = false;

    filesToLint.forEach(filePath => {
        const result = lintBook(filePath);
        allResults.push(result);
        if (result.errors.length > 0) {
            hasErrors = true;
        }
    });

    if (isJsonOutput) {
        console.log(JSON.stringify(allResults, null, 2));
    } else {
        allResults.forEach(res => {
            if (res.errors.length === 0 && res.warnings.length === 0) {
                console.log(`✅ ${res.file}`);
                return;
            }

            console.log(`\n❌ ${res.file}`);
            res.errors.forEach(err => {
                let loc = '';
                if (err.page !== undefined) loc += `Page ${err.page}`;
                if (err.sentenceIndex !== undefined) loc += ` Sentence ${err.sentenceIndex}`;
                if (err.wordIndex !== undefined) loc += ` Word ${err.wordIndex}`;
                console.log(`  [ERROR] ${loc ? `(${loc.trim()}) ` : ''}${err.message}`);
            });
            res.warnings.forEach(warn => {
                let loc = warn.page !== undefined ? `(Page ${warn.page}) ` : '';
                console.log(`  [WARN]  ${loc}${warn.message}`);
            });
        });
    }

    if (hasErrors) {
        process.exit(1);
    } else {
        process.exit(0);
    }
}

if (require.main === module) {
    run();
} else {
    module.exports = {
        lintBook,
        checkTashkeelCoverage,
        checkGradeLimits,
        checkDialectPlacement,
        checkDashBan,
        checkForeignSafety
    };
}
