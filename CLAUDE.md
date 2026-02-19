# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this repository?

**Unhandled Exception** — Blog tecnico personale di Emanuele Garofalo (Solution Architect).
Hosted su GitHub Pages all'indirizzo https://blog.unhandledexception.it.

## Stack tecnologico

- **Generatore statico**: Jekyll 4 (Ruby 3.3)
- **Tema**: [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) v4.26.2 (remote theme, skin `dark`)
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions (`.github/workflows/pages-deploy.yml`)
- **Testing**: pytest + Python 3.12
- **Dipendenze**: `Gemfile` (Ruby), Dependabot per aggiornamenti automatici

## Struttura del progetto

```
_config.yml              # Configurazione Jekyll principale
_data/navigation.yml     # Menu di navigazione del sito
_pages/                  # Pagine statiche (about, archive, categories, tags, old-articles)
_posts/                  # Articoli del blog (Markdown con front matter YAML)
assets/                  # Immagini e icone (favicon, immagini post)
tests/
  test_source.py         # Validazione sorgenti (pre-build)
  test_build.py          # Validazione output (post-build)
script/test.sh           # Script per eseguire test localmente
index.html               # Homepage
CNAME                    # Dominio custom (blog.unhandledexception.it)
Gemfile                  # Dipendenze Ruby
```

## Convenzioni importanti

### Post
- Ogni post va in `_posts/` con formato nome file: `YYYY-M-D-titolo.md`
- Front matter obbligatorio: `title`, `date`, `hidden: true`
- Tutti i post esistenti sono archiviati (`hidden: true`) e visibili solo nella pagina "Old Articles"
- Layout di default per i post: `single` (definito in `_config.yml` defaults)
- Permalink basati sulla data (es. `/2018/07/27/Un-Anno-Da-Freelance-Retrospettiva`)

### Pagine
- Le pagine statiche vanno in `_pages/` con front matter che include `permalink`
- Layout di default per le pagine: `single` con `author_profile: true`

### Navigazione
- Il menu di navigazione è definito in `_data/navigation.yml`
- Voci attuali: Categorie, Tags, Archivio, Old Articles, About

## Come eseguire i test

```bash
# Test completo (sorgenti + build + output)
bash script/test.sh

# Solo test sorgenti (non richiede build)
python3 -m pytest tests/test_source.py -v

# Singolo test (usa -k per filtrare per nome)
python3 -m pytest tests/test_source.py -v -k "test_has_theme"

# Solo test build output (richiede build precedente)
bundle exec jekyll build
python3 -m pytest tests/test_build.py -v
```

## Come fare build locale

```bash
bundle install
bundle exec jekyll serve
# Il sito sarà disponibile su http://localhost:4000
```

## CI/CD Pipeline

Il workflow GitHub Actions (`.github/workflows/pages-deploy.yml`) si attiva su push a `master`:
1. Esegue `test_source.py` (validazione sorgenti)
2. Build Jekyll con `JEKYLL_ENV=production`
3. Esegue `test_build.py` (validazione output)
4. Deploy su GitHub Pages

## Note per gli assistenti AI

- **NON rimuovere `hidden: true`** dai post esistenti senza conferma esplicita
- I test verificano che tutti i post abbiano `hidden: true` — modifiche a questo campo fanno fallire i test
- Il blog è stato migrato da Chirpy a Minimal Mistakes — i test verificano l'assenza di residui Chirpy
- Non ci sono layout, SASS o JS custom — tutto viene dal tema remote Minimal Mistakes
- Il `Gemfile.lock` è escluso dal versioning (presente in `.gitignore`)
- La lingua principale del sito è italiano (`locale: it-IT`)
- Il campo `repository` in `_config.yml` è richiesto dal plugin `jekyll-github-metadata` — senza di esso la CI fallisce con "No repo name found"
- Il `Gemfile` include `faraday-retry` come dipendenza diretta (richiesta da `github-pages` gem)
