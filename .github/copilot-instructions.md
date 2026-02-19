# Copilot Instructions — gar-ema.github.io

## Repository Overview

This is **Unhandled Exception**, a personal tech blog by Emanuele Garofalo, built with Jekyll and hosted on GitHub Pages at https://blog.unhandledexception.it.

## Tech Stack

- **Jekyll 4** (Ruby 3.3) with **Minimal Mistakes** theme v4.26.2 (remote, dark skin)
- **GitHub Pages** hosting with **GitHub Actions** CI/CD
- **pytest** (Python 3.12) for pre-build and post-build validation
- Primary language: **Italian** (`locale: it-IT`)

## Project Structure

- `_config.yml` — Main Jekyll configuration
- `_data/navigation.yml` — Site navigation menu
- `_pages/` — Static pages (about, archive, categories, tags, old-articles)
- `_posts/` — Blog posts in Markdown (YYYY-M-D-title.md format)
- `assets/` — Images and icons
- `tests/test_source.py` — Source validation tests (pre-build)
- `tests/test_build.py` — Build output validation tests (post-build)
- `script/test.sh` — Local test runner script

## Key Conventions

### Blog Posts
- File naming: `YYYY-M-D-title.md` in `_posts/`
- Required front matter: `title`, `date`, `hidden: true`
- All existing posts are archived (`hidden: true`) — visible only on the "Old Articles" page
- Default layout: `single` (configured in `_config.yml`)

### Pages
- Static pages go in `_pages/` with a `permalink` in front matter
- Default layout: `single` with `author_profile: true`

### Navigation
- Defined in `_data/navigation.yml`
- Current entries: Categorie, Tags, Archivio, Old Articles, About

## Running Tests

```bash
# Full test suite (source + build + output)
bash script/test.sh

# Source validation only (no build needed)
python3 -m pytest tests/test_source.py -v

# Build output tests (requires prior build)
bundle exec jekyll build && python3 -m pytest tests/test_build.py -v
```

## Local Development

```bash
bundle install
bundle exec jekyll serve
# Site available at http://localhost:4000
```

## Important Rules

- **Do NOT remove `hidden: true`** from existing posts without explicit confirmation — tests enforce this
- The blog was migrated from Chirpy to Minimal Mistakes — tests check for absence of Chirpy leftovers
- No custom layouts, SASS, or JS — everything comes from the remote Minimal Mistakes theme
- `Gemfile.lock` is gitignored
- The CI/CD pipeline runs on push to `master`: source tests → Jekyll build → output tests → deploy
