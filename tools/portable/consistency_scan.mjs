import fs from 'fs/promises';
import path from 'path';

const ANTONYM_PAIRS = [
  ['increase', 'decrease'],
  ['rise', 'fall'],
  ['more', 'less'],
  ['above', 'below'],
  ['left', 'right'],
  ['positive', 'negative'],
  ['buyer', 'seller'],
  ['elastic', 'inelastic'],
  ['true', 'false'],
  ['high', 'low'],
  ['up', 'down'],
  ['short', 'long']
];

const STOP_WORDS = new Set([
  "a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"
]);

function tokenize(text) {
  return text.toLowerCase().replace(/[^\w\s]/g, ' ').split(/\s+/).filter(w => w);
}

function getSentences(text) {
  return text.split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(s => s);
}

export function extractTerms(items) {
  const terms = new Set();
  const phraseCounts = new Map();
  
  for (const item of items) {
    if (!item.text) continue;
    const text = item.text;
    
    const capMatches = text.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b/g);
    if (capMatches) {
      for (const match of capMatches) {
        terms.add(match.toLowerCase());
      }
    }
    
    const tokens = tokenize(text);
    for (let i = 0; i < tokens.length - 1; i++) {
      if (STOP_WORDS.has(tokens[i]) || STOP_WORDS.has(tokens[i+1])) continue;
      const bigram = `${tokens[i]} ${tokens[i+1]}`;
      phraseCounts.set(bigram, (phraseCounts.get(bigram) || 0) + 1);
      
      if (i < tokens.length - 2) {
        if (!STOP_WORDS.has(tokens[i+2])) {
          const trigram = `${tokens[i]} ${tokens[i+1]} ${tokens[i+2]}`;
          phraseCounts.set(trigram, (phraseCounts.get(trigram) || 0) + 1);
        }
      }
    }
  }
  
  for (const [phrase, count] of phraseCounts.entries()) {
    if (count >= 2) {
      terms.add(phrase);
    }
  }
  
  return Array.from(terms);
}

const DEFINITION_PATTERNS = [
  "is", "are", "means", "refers to", "is defined as", "are defined as"
];

function isDefinitional(sentence, term) {
  const lowerSentence = sentence.toLowerCase();
  const lowerTerm = term.toLowerCase();
  
  if (!lowerSentence.includes(lowerTerm)) return false;
  
  for (const pattern of DEFINITION_PATTERNS) {
    const regex = new RegExp(`\\b${lowerTerm}\\s+${pattern}\\b`, 'i');
    if (regex.test(lowerSentence)) return true;
  }
  return false;
}

function getJaccard(setA, setB) {
  if (setA.size === 0 && setB.size === 0) return 1.0;
  const intersection = new Set([...setA].filter(x => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return intersection.size / union.size;
}

function getContentWords(sentence) {
  return new Set(tokenize(sentence).filter(w => !STOP_WORDS.has(w)));
}

function extractNumbers(sentence) {
  const regex = /\b\d+(?:\.\d+)?(?:\s*[a-zA-Z%]+)?\b/g;
  return sentence.match(regex) || [];
}

const JACCARD_THRESHOLD = 0.2;

function checkConflict(sent1, sent2) {
  const reasons = [];
  const words1 = getContentWords(sent1);
  const words2 = getContentWords(sent2);
  
  const jaccard = getJaccard(words1, words2);
  
  if (jaccard < JACCARD_THRESHOLD) {
    reasons.push(`Low lexical overlap (Jaccard ${jaccard.toFixed(2)})`);
  }
  
  for (const [w1, w2] of ANTONYM_PAIRS) {
    if ((words1.has(w1) && words2.has(w2)) || (words1.has(w2) && words2.has(w1))) {
      reasons.push(`Antonym mismatch ('${w1}' vs '${w2}')`);
    }
  }
  
  const sent1Lower = sent1.toLowerCase();
  const sent2Lower = sent2.toLowerCase();
  
  for (const word of words1) {
    if (sent2Lower.includes(`not ${word}`) || sent2Lower.includes(`never ${word}`)) {
      reasons.push(`Negation mismatch ('${word}' negated)`);
    }
  }
  for (const word of words2) {
    if (sent1Lower.includes(`not ${word}`) || sent1Lower.includes(`never ${word}`)) {
      reasons.push(`Negation mismatch ('${word}' negated)`);
    }
  }

  const nums1 = new Set(extractNumbers(sent1Lower));
  const nums2 = new Set(extractNumbers(sent2Lower));
  
  if (nums1.size > 0 && nums2.size > 0) {
    for (const n1 of nums1) {
      for (const n2 of nums2) {
        if (n1 !== n2 && !nums1.has(n2) && !nums2.has(n1)) {
          reasons.push(`Numeric mismatch ('${n1}' vs '${n2}')`);
        }
      }
    }
  }
  
  return {
    conflict: reasons.length > 0,
    reasons: [...new Set(reasons)],
    overlap: jaccard
  };
}

export function scanConsistency(items, glossaryTerms = null) {
  let terms = [];
  if (glossaryTerms) {
    terms = glossaryTerms;
  } else {
    terms = extractTerms(items);
  }
  
  const conflicts = [];
  let termsScanned = 0;
  
  for (const term of terms) {
    const defs = [];
    
    for (const item of items) {
      if (!item.text) continue;
      const sentences = getSentences(item.text);
      for (const sentence of sentences) {
        if (isDefinitional(sentence, term)) {
          defs.push({
            id: item.id,
            ref: item.ref,
            surface: item.surface,
            sentence: sentence
          });
        }
      }
    }
    
    if (defs.length >= 2) {
      termsScanned++;
      for (let i = 0; i < defs.length; i++) {
        for (let j = i + 1; j < defs.length; j++) {
          const res = checkConflict(defs[i].sentence, defs[j].sentence);
          if (res.conflict) {
            conflicts.push({
              term,
              items: [defs[i], defs[j]],
              reason: res.reasons.join('; '),
              overlap: res.overlap
            });
          }
        }
      }
    }
  }
  
  return {
    conflicts,
    meta: {
      terms_scanned: termsScanned,
      conflicts: conflicts.length
    }
  };
}

async function main() {
  const args = process.argv.slice(2);
  let itemsPath = null;
  let glossaryPath = null;
  let useJson = false;
  
  for (const arg of args) {
    if (arg === '--json') {
      useJson = true;
    } else if (!itemsPath) {
      itemsPath = arg;
    } else if (!glossaryPath) {
      glossaryPath = arg;
    }
  }
  
  if (!itemsPath) {
    console.error("Usage: node consistency_scan.mjs <items.json> [glossary.json] [--json]");
    process.exit(1);
  }
  
  let items = [];
  try {
    items = JSON.parse(await fs.readFile(itemsPath, 'utf8'));
  } catch(e) {
    console.error("Error reading items file:", e.message);
    process.exit(1);
  }
  
  let glossaryTerms = null;
  if (glossaryPath) {
    try {
      const glossary = JSON.parse(await fs.readFile(glossaryPath, 'utf8'));
      glossaryTerms = Object.keys(glossary);
    } catch(e) {
      console.error("Error reading glossary file:", e.message);
      process.exit(1);
    }
  }
  
  const result = scanConsistency(items, glossaryTerms);
  
  if (useJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`Consistency Scan Report`);
    console.log(`Terms scanned with multiple definitions: ${result.meta.terms_scanned}`);
    console.log(`Conflicts found: ${result.meta.conflicts}\n`);
    
    const byTerm = {};
    for (const c of result.conflicts) {
      if (!byTerm[c.term]) byTerm[c.term] = [];
      byTerm[c.term].push(c);
    }
    
    for (const [term, termConflicts] of Object.entries(byTerm)) {
      console.log(`=== Term: "${term}" ===`);
      for (const c of termConflicts) {
        console.log(`Reason: ${c.reason}`);
        console.log(`  [${c.items[0].id}] ${c.items[0].sentence}`);
        console.log(`  [${c.items[1].id}] ${c.items[1].sentence}`);
      }
      console.log();
    }
  }
}

// Check if running as main
import { fileURLToPath } from 'url';
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch(console.error);
}
