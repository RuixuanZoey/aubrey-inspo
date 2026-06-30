const fs = require('fs');
const path = require('path');

const inspDir = path.join(__dirname, '..', 'src', 'content', 'inspirations');
const files = fs.readdirSync(inspDir).filter(f => f.endsWith('.md')).sort();

const data = [];

for (const file of files) {
  const content = fs.readFileSync(path.join(inspDir, file), 'utf-8');
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) continue;

  const raw = frontmatterMatch[1];
  const fields = {};
  let currentKey = '';
  for (const line of raw.split('\n')) {
    const match = line.match(/^(\w+):\s*(.*)/);
    if (match) {
      currentKey = match[1];
      let val = match[2].trim();
      if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
      fields[currentKey] = val;
    }
  }

  const num = parseInt(file.match(/\d+/)[0]);

  data.push({
    id: num,
    slug: file.replace('.md', ''),
    image: fields.image || '',
    title: fields.title || '',
    style: fields.style || '',
    colorScheme: fields.colorScheme || '',
    layout: fields.layout || '',
    note: fields.note || '',
    source: fields.source || '',
    createdAt: fields.createdAt || '',
    sha: ''  // will be populated from GitHub API
  });
}

// Output without SHA (will be added later)
const outPath = path.join(__dirname, '..', 'public', 'data.json');
fs.writeFileSync(outPath, JSON.stringify(data, null, 2));
console.log(`Generated data.json with ${data.length} entries`);
console.log('Slugs:', data.map(d => d.slug).join(', '));
