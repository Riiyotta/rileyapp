#!/usr/bin/env node
/**
 * Re-measure section heights of the BUILT clone (optional tool; verify_all.py never runs it).
 *
 *   npm ci && npx vite build --outDir <scratch-dir>
 *   npx vite preview --outDir <scratch-dir> --port <port>
 *   NODE_PATH="$(npm root -g)" RILEY_BASE_URL=http://localhost:<port> node design-repo/extraction/measure_sections.mjs > heights.json
 *
 * Playwright is resolved through NODE_PATH (a global install); no machine path is stored here.
 * Output: { viewport: { template: { route, pageHeight, sections: [{ section, index, top, height }] } } }
 * One representative route per template (plus /blog/health, the empty-category variant).
 * Section boundaries come from the rendered DOM: page wrappers are split into their real children, and
 * long-form bodies are split at their real heading boundaries (article h2 chapters, text-page h3 chapters).
 */
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = process.env.RILEY_BASE_URL || 'http://localhost:4173';
const VIEWPORTS = (process.env.RILEY_VIEWPORTS || '1440,768,390').split(',').map(Number);

export const ROUTES = {
  home: '/',
  pricing: '/pricing',
  'not-found': '/baby-tracker',
  'blog-index': '/blog',
  'blog-category': '/blog/sleep',
  'blog-category:empty': '/blog/health',
  'blog-article': '/blog/sleep/baby-witching-hour',
  'text-page': '/editorial-process',
  legal: '/tos',
};

// Runs in the page. Returns [{section, top, bottom}] in document coordinates.
function resolveSections(template) {
  const R = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { top: r.top + window.scrollY, bottom: r.bottom + window.scrollY };
  };
  const kids = (el) => (el ? [...el.children] : []);
  const root = document.getElementById('root');
  const top = kids(root);
  const out = [];
  const push = (section, el) => {
    const b = el && el.top !== undefined ? el : R(el);
    if (b) out.push({ section, top: b.top, bottom: b.bottom });
    else out.push({ section, top: null, bottom: null });
  };
  const announce = () => push('announcement-bar', document.querySelector('aside')?.parentElement);
  const header = () => push('site-header', document.querySelector('header.upper-header-in'));
  const finalCta = () => push('final-cta', [...document.querySelectorAll('section')].find((s) => s.querySelector('img[alt="Background decoration"]')));
  const footer = () => push('site-footer', document.querySelector('footer'));

  if (template === 'home') {
    announce();
    header();
    const heroHeader = document.querySelector('header.upper-header-in').parentElement;
    const press = heroHeader.lastElementChild;
    push('hero-home', { top: R(document.querySelector('header.upper-header-in')).bottom, bottom: R(press).top });
    push('press-marquee', press);
    const ids = ['personalization-marquee', 'superpowers-grid', 'featurette-carousel', 'clinical-board', 'how-riley-works',
      'testimonials-carousel', 'gradient-band', 'faq-clouds', 'blog-teaser'];
    top.slice(2, 2 + ids.length).forEach((el, i) => push(ids[i], el));
    finalCta();
    footer();
  } else if (template === 'pricing') {
    announce();
    header();
    const wrap = top[1];
    const ids = ['pricing-hero', 'testimonials-carousel', 'gradient-band', 'faq-clouds'];
    kids(wrap).slice(1, 1 + ids.length).forEach((el, i) => push(ids[i], el));
    finalCta();
    footer();
  } else if (template === 'not-found') {
    announce();
    header();
    push('not-found-block', top[2]);
    footer();
  } else if (template.startsWith('blog-index') || template.startsWith('blog-category')) {
    if (template === 'blog-index') announce();
    header();
    const col = document.querySelector('div.mt-\\[5rem\\]');
    const [hero, search, list] = kids(col);
    push('blog-index-hero', hero);
    push('blog-search', search);
    const [tabs, grid] = kids(list);
    push('blog-category-tabs', tabs);
    const gk = kids(grid);
    const featured = gk.find((c) => c.classList.contains('col-span-full'));
    const cards = gk.find((c) => !c.classList.contains('col-span-full'));
    if (featured) push('blog-featured-banner', featured);
    if (cards) push('blog-post-grid', cards);
    push('blog-pagination', col.parentElement.nextElementSibling);
    finalCta();
    footer();
  } else if (template === 'blog-article') {
    header();
    const col8 = document.querySelector('article > div > div');
    push('article-top-bar', kids(col8).slice(0, 2).find((d) => d.getBoundingClientRect().height > 0));
    const h1 = [...document.querySelectorAll('article h1')].find((h) => h.getBoundingClientRect().height > 0);
    const headerBlock = h1.closest('div.gap-\\[4\\.5rem\\]');
    push('article-header', headerBlock);
    const toc = [...document.querySelectorAll('article nav')].find((n) => n.querySelector('ul a[href^="#"]') && n.getBoundingClientRect().height > 0);
    push('article-toc', toc.closest('div.sticky') || toc.parentElement);
    const body = document.querySelector('.ab-body');
    const b = R(body);
    const h2s = [...body.querySelectorAll(':scope > h2.ab-h2')].map((h) => R(h).top);
    push('article-intro', { top: b.top, bottom: h2s[0] ?? b.bottom });
    h2s.forEach((t, i) => push('article-chapter', { top: t, bottom: h2s[i + 1] ?? b.bottom }));
    const prose = body.parentElement;
    push('article-sources', kids(prose)[1]);
    push('article-share-row', kids(prose)[2]);
    const contentCol = headerBlock.parentElement;
    const related = kids(contentCol).filter((c) => c.querySelector('h3.h3-small'));
    push('article-related-posts', related[0]);
    finalCta();
    footer();
  } else if (template === 'text-page') {
    announce();
    header();
    const sec = document.querySelector('section.tp-prose');
    const s = R(sec);
    const h3s = [...sec.querySelectorAll(':scope > h3')].map((h) => R(h).top);
    const closing = R(sec.querySelector('p.tp-closing'));
    push('text-page-header', { top: s.top, bottom: h3s[0] });
    h3s.forEach((t, i) => push('text-page-chapter', { top: t, bottom: h3s[i + 1] ?? closing.top }));
    push('text-page-closing', { top: closing.top, bottom: s.bottom });
    footer();
  } else if (template === 'legal') {
    announce();
    header();
    push('legal-policy-embed', document.querySelector('main'));
    footer();
  }
  return out;
}

async function measure(page, template, route) {
  await page.goto(BASE + route, { waitUntil: 'networkidle' });
  // trigger lazy images, then return to top
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h; y += 700) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(60);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(400);
  const res = await page.evaluate(resolveSections, template.split(':')[0]);
  const pageHeight = await page.evaluate(() => document.documentElement.scrollHeight);
  const counts = {};
  return {
    route,
    pageHeight,
    sections: res.map((s) => {
      counts[s.section] = (counts[s.section] || 0) + 1;
      return {
        section: s.section,
        index: counts[s.section] - 1,
        top: s.top === null ? null : Math.round(s.top),
        height: s.top === null ? null : Math.round(s.bottom - s.top),
      };
    }),
  };
}

const browser = await chromium.launch();
const result = {};
for (const vw of VIEWPORTS) {
  const page = await browser.newPage({ viewport: { width: vw, height: 900 } });
  result[vw] = {};
  for (const [template, route] of Object.entries(ROUTES)) {
    result[vw][template] = await measure(page, template, route);
  }
  await page.close();
}
await browser.close();
process.stdout.write(JSON.stringify(result, null, 1) + '\n');
