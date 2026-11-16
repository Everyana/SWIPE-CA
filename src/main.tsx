import React,{useMemo,useRef,useState,useEffect} from 'react';
import{createRoot}from'react-dom/client';
import{Search,Bookmark,Share2,ExternalLink,ArrowUp,ArrowDown,Check,Menu,X}from'lucide-react';
import './style.css';
type Lang='en'|'fr';type Story={id:string,category:string,jurisdiction:string,date:string,language:Lang,deadline?:string,en:{title:string,summary:string,action:string},fr:{title:string,summary:string,action:string},source:string,url:string};
const tr={en:{tag:'DO THE SWIPE',sub:'Public information. One swipe at a time.',search:'Search public updates',all:'All topics',every:'All jurisdictions',official:'Official source',save:'Save',saved:'Saved',share:'Share',empty:'No cards match your filters.',reset:'Clear filters',help:'Scroll or use ↑ ↓ to swipe',sources:'Sources',about:'About',aboutText:'SWIPES brings together selected notices from official Canadian sources. Browse by topic or jurisdiction and open the original notice for full details. The interface is available in English and French. Notices appear in the language used by the issuing source.',close:'Close'},fr:{tag:'FAITES LE SWIPE',sub:'L’information publique. Un swipe à la fois.',search:'Rechercher les nouvelles publiques',all:'Tous les sujets',every:'Toutes les administrations',official:'Source officielle',save:'Enregistrer',saved:'Enregistré',share:'Partager',empty:'Aucune carte ne correspond.',reset:'Effacer les filtres',help:'Défilez ou utilisez ↑ ↓',sources:'Sources',about:'À propos',aboutText:'SWIPES rassemble une sélection d’avis de sources officielles canadiennes. Parcourez-les par sujet ou par administration et ouvrez l’avis original pour tous les détails. L’interface est offerte en français et en anglais. Les avis sont présentés dans la langue utilisée par l’organisme qui les publie.',close:'Fermer'}};
const jurisdictions = {
  Federal: 'Fédéral', Alberta: 'Alberta', 'British Columbia': 'Colombie-Britannique',
  Manitoba: 'Manitoba', 'New Brunswick': 'Nouveau-Brunswick',
  'Newfoundland and Labrador': 'Terre-Neuve-et-Labrador',
  'Northwest Territories': 'Territoires du Nord-Ouest', 'Nova Scotia': 'Nouvelle-Écosse',
  Nunavut: 'Nunavut', Ontario: 'Ontario', 'Prince Edward Island': 'Île-du-Prince-Édouard',
  Quebec: 'Québec', Saskatchewan: 'Saskatchewan', Yukon: 'Yukon',
};
const topics = {
  'Public updates': 'Actualités publiques', 'Jobs and training': 'Emploi et formation',
  'Education': 'Éducation', 'Health': 'Santé', 'Transport': 'Transports',
  'Housing': 'Logement', 'Environment': 'Environnement', 'Public safety': 'Sécurité publique',
  'Public consultations': 'Consultations publiques', 'Grants and funding': 'Subventions et financement',
  'Immigration': 'Immigration', 'Tenders': 'Appels d’offres', 'Sport and recreation': 'Sports et loisirs',
};
function label(value: string, translations: Record<string, string>, lang: Lang) {
  return lang === 'fr' ? translations[value] ?? value : value;
}
function searchText(value: string) {
  return value.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim();
}

function App(){const[lang,setLang]=useState<Lang>('en');const[stories,setStories]=useState<Story[]>([]);const[feedStatus,setFeedStatus]=useState<'loading'|'live'|'unavailable'|'empty'>('loading');const[feedUpdated,setFeedUpdated]=useState('');const [retry, setRetry] = useState(0);
useEffect(() => {
  let request: AbortController | undefined;
  let latestTimestamp = 0;

  async function fetchFeed(url: string, signal: AbortSignal) {
    const response = await fetch(url, {cache: 'no-cache', signal, credentials: 'omit'});
    if (!response.ok) throw Error('Notices unavailable');
    const data = await response.json();
    if (!Array.isArray(data.notices)) throw Error('Invalid notice feed');
    return data;
  }
  async function load() {
    request?.abort();
    const controller = new AbortController();
    request = controller;
    const timeout = window.setTimeout(() => controller.abort(), 10000);
    try {
      const results = await Promise.allSettled([
        fetchFeed('/data/notices.json', controller.signal),
        fetchFeed('https://raw.githubusercontent.com/Everyana/SWIPE-CA/main/public/data/notices.json', controller.signal),
      ]);
      if (controller.signal.aborted && request !== controller) return;
      const feeds = results.flatMap(result => result.status === 'fulfilled' ? [result.value] : []);
      const data = feeds.sort((a, b) => (Date.parse(b.updatedAt) || 0) - (Date.parse(a.updatedAt) || 0))[0];
      if (!data) throw Error('Notices unavailable');
      const timestamp = Date.parse(data.updatedAt) || 0;
      if (timestamp < latestTimestamp) return;
      const valid = data.notices.filter((n: any) =>
        n && typeof n.id === 'string' && typeof n.title === 'string' &&
        typeof n.url === 'string' && /^https:\/\//.test(n.url) &&
        typeof n.publishedAt === 'string' && Number.isFinite(Date.parse(n.publishedAt))
      ).map((n: any): Story => ({
        id: n.id, category: n.category || 'Public updates', jurisdiction: n.jurisdiction || 'Canada',
        date: n.publishedAt, language: n.language === 'fr' ? 'fr' : 'en',
        en: {title: n.title, summary: n.summary || n.title, action: 'Read original notice'},
        fr: {title: n.title, summary: n.summary || n.title, action: 'Lire l’avis original'},
        source: n.source, url: n.url,
      }));
      if (request === controller) {
        latestTimestamp = timestamp;
        setStories(valid);
        setFeedUpdated(data.updatedAt || '');
        setFeedStatus(valid.length ? 'live' : 'empty');
      }
    } catch {
      if (request === controller) setFeedStatus('unavailable');
    } finally {
      window.clearTimeout(timeout);
    }
  }
  void load();
  const timer = window.setInterval(() => { if (!document.hidden) void load(); }, 300000);
  function refreshOnReturn() { if (!document.hidden) void load(); }
  document.addEventListener('visibilitychange', refreshOnReturn);
  return () => {
    const pending = request;
    request = undefined;
    pending?.abort();
    window.clearInterval(timer);
    document.removeEventListener('visibilitychange', refreshOnReturn);
  };
}, [retry]);
const[q,setQ]=useState('');const[cat,setCat]=useState('All');const[jur,setJur]=useState('All');const[saved,setSaved]=useState<string[]>(()=>{try{return JSON.parse(localStorage.getItem('swipes-saved')||'[]')}catch{return []}});const[active,setActive]=useState(0);const[modal,setModal]=useState(false);const feed=useRef<HTMLDivElement>(null);const t=tr[lang];const cats = ['All', ...new Set(stories.map(s => s.category))];
const jurs = ['All', ...new Set([...Object.keys(jurisdictions),...stories.map(s=>s.jurisdiction)])];
const hasFilters = !!q.trim() || cat !== 'All' || jur !== 'All';
const filtered = useMemo(() => stories.filter(s =>
  (cat === 'All' || s.category === cat) && (jur === 'All' || s.jurisdiction === jur) &&
  searchText(`${s.en.title} ${s.en.summary} ${s.source} ${s.category} ${s.jurisdiction} ${label(s.category, topics, 'fr')} ${label(s.jurisdiction, jurisdictions, 'fr')}`).includes(searchText(q))
), [stories, q, cat, jur]);
useEffect(()=>{localStorage.setItem('swipes-saved',JSON.stringify(saved))},[saved]);useEffect(()=>{setActive(0);feed.current?.scrollTo({top:0,behavior:'instant' as ScrollBehavior})},[q,cat,jur]);useEffect(()=>{const fn=(e:KeyboardEvent)=>{if((e.target as HTMLElement)?.matches('input,select,textarea'))return;if(!modal && filtered.length && (e.key==='ArrowDown'||e.key==='ArrowUp')){e.preventDefault();const next=Math.max(0,Math.min(filtered.length-1,active+(e.key==='ArrowDown'?1:-1)));feed.current?.children[next]?.scrollIntoView({block:'start',behavior:'smooth'});setActive(next)}};window.addEventListener('keydown',fn);return()=>window.removeEventListener('keydown',fn)},[active,filtered.length,modal]);useEffect(()=>{document.documentElement.lang=lang},[lang]);
useEffect(() => {
  if (!stories.length || !location.hash) return;
  const card = Array.from(feed.current?.children ?? []).find(el => encodeURIComponent(el.id) === location.hash.slice(1));
  card?.scrollIntoView({block: 'start'});
}, [stories.length]);
const toggle=(id:string)=>setSaved(s=>s.includes(id)?s.filter(x=>x!==id):[...s,id]);const share=async(s:Story)=>{const data={title:s[lang].title,text:s[lang].summary,url:location.href.split('#')[0]+'#'+encodeURIComponent(s.id)};try{if(navigator.share)await navigator.share(data);else await navigator.clipboard.writeText(data.url)}catch{}};return <div className="shell"><header><button type="button" className="brand" aria-label="Return to first story" onClick={()=>{setQ('');setCat('All');setJur('All');setActive(0);history.replaceState(null,'',location.pathname);feed.current?.scrollTo({top:0,behavior:'instant' as ScrollBehavior})}}><div className="logo" aria-hidden="true"><svg viewBox="0 0 64 64" role="img"><path d="M32 5 37 17 44 12 43 23 55 20 49 30 59 34 45 40 47 48 35 45 35 59 29 59 29 45 17 48 19 40 5 34 15 30 9 20 21 23 20 12 27 17Z" fill="currentColor"/></svg></div><div><strong>SWIPES<span className="dot">.</span></strong><small>{lang==='en'?'CANADA EDITION · PUBLIC INFORMATION':'ÉDITION CANADIENNE · INFORMATION PUBLIQUE'}</small></div></button><nav><span className="tag">{lang==='en'?'MADE FOR CANADA':'POUR LE CANADA'}</span><div className="language-options" role="group" aria-label={lang==='en'?'Interface language':'Langue de l’interface'}>
  <button className="lang" onClick={()=>setLang('en')} aria-label="English" aria-pressed={lang==='en'}>EN</button>
  <button className="lang" onClick={()=>setLang('fr')} aria-label="Français" aria-pressed={lang==='fr'}>FR</button>
</div><button className="iconbtn" onClick={()=>setModal(true)} aria-label={t.about}><Menu size={22}/></button></nav></header><div className="toolbar"><label className="search"><Search size={18}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder={t.search} aria-label={t.search}/></label><select aria-label={lang==='en'?'Topic':'Sujet'} value={cat} onChange={e=>setCat(e.target.value)}>{cats.map(c=><option key={c} value={c}>{c==='All'?t.all:label(c,topics,lang)}</option>)}</select><select aria-label={lang==='en'?'Jurisdiction':'Administration'} value={jur} onChange={e=>setJur(e.target.value)}>{jurs.map(c=><option key={c} value={c}>{c==='All'?t.every:label(c,jurisdictions,lang)}</option>)}</select></div><div className="content"><aside className="rail"><div className="railTitle">{lang==='en'?'THE CANADIAN PUBLIC FEED':'LE FIL PUBLIC CANADIEN'}</div><h2 className="railHeadline">{lang==='en'?'Know what matters.\nFrom coast to coast.':'L’essentiel public.\nD’un océan à l’autre.'}</h2><p>{t.sub}</p><div className="railMaple" aria-hidden="true">✦</div><div className="railCounter"><strong>{filtered.length}</strong><span>{feedStatus==='live'?'OFFICIAL NOTICES':'NOTICES'}</span></div><p className="railHelp"><ArrowDown size={15}/>{t.help}</p><div className="railFoot">{lang==='en'?'INDEPENDENT PUBLIC-INFORMATION DISCOVERY · NOT A GOVERNMENT WEBSITE':'DÉCOUVERTE INDÉPENDANTE · SITE NON GOUVERNEMENTAL'}</div></aside><main className="reader" ref={feed} onScroll={e=>{const el=e.currentTarget;const top=el.getBoundingClientRect().top; const cards=Array.from(el.querySelectorAll('article.story')); const next=cards.findIndex(card=>card.getBoundingClientRect().top>top+1); setActive(next<0?Math.max(0,cards.length-1):Math.max(0,next-1))}}>{filtered.length===0?<div className="empty" role="status"><h2>{
  feedStatus==='loading' ? (lang==='en'?'Loading official notices…':'Chargement des avis officiels…') :
  feedStatus==='unavailable' ? (lang==='en'?'Official notices could not be loaded.':'Impossible de charger les avis officiels.') :
  stories.length && hasFilters ? t.empty :
  (lang==='en'?'No official notices are published in this feed yet.':'Aucun avis officiel n’est encore publié dans ce fil.')
}</h2>{feedStatus==='unavailable' ?
  <button onClick={()=>{setFeedStatus('loading');setRetry(value=>value+1)}}>{lang==='en'?'Try again':'Réessayer'}</button> :
  !!stories.length && hasFilters && <button onClick={()=>{setQ('');setCat('All');setJur('All')}}>{t.reset}</button>
}</div>:filtered.map((s,i)=><article className="story" id={s.id} key={s.id}><div className="storyInner"><div className="meta"><span className="pill">{label(s.category,topics,lang)}</span><span>{label(s.jurisdiction,jurisdictions,lang)}</span><span className="sep">·</span><span>{new Date(s.date).toLocaleDateString(lang==='fr'?'fr-CA':'en-CA',{year:'numeric',month:'short',day:'numeric',timeZone:'UTC'})}</span></div><div className="notice-language">{lang==='en'?'Original language':'Langue originale'} · {s.language==='fr'?'Français':'English'}</div><h1 lang={s.language}>{s[lang].title}</h1>{s[lang].summary!==s[lang].title&&<p className="summary" lang={s.language}>{s[lang].summary}</p>}{s.deadline&&<div className="deadline">{lang==='en'?'Deadline':'Date limite'}: {s.deadline}</div>}<a className="source notice-source" href={s.url} target="_blank" rel="noopener noreferrer">
  <div><span>{t.official}</span><strong>{s.source}</strong></div>
  <span className="source-action">{s[lang].action}<ExternalLink size={16} aria-hidden="true"/></span>
</a><div className="actions"><button onClick={()=>toggle(s.id)}>{saved.includes(s.id)?<Check size={19}/>:<Bookmark size={19}/>} {saved.includes(s.id)?t.saved:t.save}</button><button onClick={()=>share(s)}><Share2 size={19}/>{t.share}</button><span className="count">{String(i+1).padStart(2,'0')} / {String(filtered.length).padStart(2,'0')}</span></div></div></article>)}</main><aside className="rightRail"><div className="vertical">SWIPE TO KNOW · SWIPE TO KNOW · SWIPE TO KNOW</div><div className="arrows"><button onClick={()=>feed.current?.children[Math.max(0,active-1)]?.scrollIntoView({behavior:'smooth'})} aria-label="Previous"><ArrowUp size={20}/></button><button onClick={()=>feed.current?.children[Math.min(filtered.length-1,active+1)]?.scrollIntoView({behavior:'smooth'})} aria-label="Next"><ArrowDown size={20}/></button></div></aside></div><footer><span>SWIPES · CANADA / CANADA</span><span>{feedStatus==='live'?(lang==='en'?'OFFICIAL SOURCES · ORIGINAL-LANGUAGE EXCERPTS':'SOURCES OFFICIELLES · EXTRAITS EN LANGUE ORIGINALE'):(lang==='en'?'LIVE FEED NOT YET AVAILABLE':'FLUX EN DIRECT NON DISPONIBLE')}</span></footer>{modal&&<div className="overlay" onClick={()=>setModal(false)}><section className="modal" onClick={e=>e.stopPropagation()}><button className="close" onClick={()=>setModal(false)}><X/></button><h2>{t.about} SWIPES</h2><p>{t.aboutText}</p><p>{lang==='en'?'Independent platform. Not affiliated with or endorsed by the Government of Canada.':'Plateforme indépendante. Non affiliée au gouvernement du Canada et non approuvée par celui-ci.'}</p><p>{lang==='en'?'Coverage in this edition':'Couverture de cette édition'} · {new Set(stories.map(s=>s.jurisdiction)).size} / {Object.keys(jurisdictions).length}</p>{feedUpdated&&<p>{lang==='en'?'Feed last refreshed':'Dernière actualisation du fil'} · <time dateTime={feedUpdated}>{new Date(feedUpdated).toLocaleString(lang==='fr'?'fr-CA':'en-CA')}</time></p>}<button className="primary" onClick={()=>setModal(false)}>{t.close}</button></section></div>}</div>}
createRoot(document.getElementById('root')!).render(<App/>);
