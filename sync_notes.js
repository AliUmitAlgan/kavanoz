const fs = require('fs');
const path = require('path');

const jsonPath = path.join(__dirname, 'notlar.json');
const htmlPath = path.join(__dirname, 'index.html');

if (!fs.existsSync(jsonPath)) {
  console.error('notlar.json bulunamadı!');
  process.exit(1);
}

const rawJson = fs.readFileSync(jsonPath, 'utf8');
const notesList = JSON.parse(rawJson);

// Sadece secildi === true olanları veya secildi belirtilmemişse hepsini al
const activeNotes = notesList.filter(n => n.secildi !== false).map(n => ({
  category: n.kategori,
  text: n.not
}));

console.log(`Seçilen aktif not sayısı: ${activeNotes.length}`);

let html = fs.readFileSync(htmlPath, 'utf8');

// 1. RAW_150_NOTES dizisini güncelle
const newRawNotesArrayStr = 'const RAW_150_NOTES = ' + JSON.stringify(activeNotes, null, 2) + ';';
html = html.replace(/const RAW_150_NOTES = \[[\s\S]*?\];/g, newRawNotesArrayStr);

// 2. Kalıcı ve güvenli Storage Key (Kullanıcının açtığı notlar asla silinmez)
const stableStorageKey = 'bebinin_yil_donumu_kavanozu';
html = html.replace(/const STORAGE_KEY = '[^']+';/g, `const STORAGE_KEY = '${stableStorageKey}';`);

// 3. Başlıktaki varsayılan sayaç değerini güncelle
html = html.replace(/<span id="headerTotalNotes"[^>]*>\d+<\/span>/g, `<span id="headerTotalNotes" class="font-bold">${activeNotes.length}</span>`);

fs.writeFileSync(htmlPath, html, 'utf8');
console.log(`index.html başarıyla güncellendi! Kalıcı storage key: ${stableStorageKey}`);
