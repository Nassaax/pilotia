// Rend le calque de texte d'un Reel terrain, image par image, sur fond transparent.
//   node reels-terrain-calque.js <url du site local> <reel> <dossier de sortie> <images/s>
// Écrit 00000.png, 00001.png… et un fichier infos.json (durée, fin, claques).
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const [,, base, reel, sortie, ips] = process.argv;
  fs.mkdirSync(sortie, { recursive: true });
  const navigateur = await chromium.launch();
  const page = await (await navigateur.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
  await page.goto(`${base}/brand/reels-terrain.html?r=${reel}`, { waitUntil: 'networkidle' });
  await page.evaluate('document.fonts.ready');
  const infos = await page.evaluate('({duree: DUREE, fin: FIN, impacts: IMPACTS})');
  fs.writeFileSync(`${sortie}/infos.json`, JSON.stringify(infos));
  const total = Math.round(infos.duree * +ips);
  for (let i = 0; i < total; i++) {
    await page.evaluate(`rendre(${i / +ips})`);
    await page.screenshot({ path: `${sortie}/${String(i).padStart(5, '0')}.png`, omitBackground: true });
  }
  await navigateur.close();
})();
