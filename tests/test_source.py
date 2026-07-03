"""Tests that validate source files without requiring a Jekyll build."""

import os
import re
import unittest
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTS_DIR = os.path.join(ROOT, "_posts")
PAGES_DIR = os.path.join(ROOT, "_pages")
DATA_DIR = os.path.join(ROOT, "_data")
CONFIG_FILE = os.path.join(ROOT, "_config.yml")


def _parse_front_matter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def _load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def _get_posts():
    return sorted(f for f in os.listdir(POSTS_DIR) if f.endswith(".md"))


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = _load_config()

    def test_config_exists(self):
        self.assertTrue(os.path.isfile(CONFIG_FILE))

    def test_has_theme(self):
        has_theme = "theme" in self.config or "remote_theme" in self.config
        self.assertTrue(has_theme, "Missing theme or remote_theme in config")
        if "theme" in self.config:
            self.assertIn("minimal-mistakes", self.config["theme"])
        if "remote_theme" in self.config:
            self.assertIn("minimal-mistakes", self.config["remote_theme"])

    def test_has_minimal_mistakes_skin(self):
        self.assertIn("minimal_mistakes_skin", self.config,
                      "Missing minimal_mistakes_skin in config")

    def test_has_required_fields(self):
        for field in ["title", "description", "url", "plugins"]:
            self.assertIn(field, self.config, f"Missing field: {field}")

    def test_plugins_include_required(self):
        plugins = self.config["plugins"]
        for p in ["jekyll-remote-theme", "jekyll-feed"]:
            self.assertIn(p, plugins, f"Missing plugin: {p}")

    def test_includes_pages_directory(self):
        includes = self.config.get("include", [])
        self.assertIn("_pages", includes, "Missing include: [_pages]")

    def test_defaults_set_layout(self):
        defaults = self.config.get("defaults", [])
        post_defaults = [d for d in defaults if d.get("scope", {}).get("type") == "posts"]
        self.assertTrue(len(post_defaults) > 0, "No defaults for posts")
        self.assertIn("layout", post_defaults[0]["values"])
        allowed_layouts = {"single", "post"}
        actual_layout = post_defaults[0]["values"]["layout"]
        self.assertIn(actual_layout, allowed_layouts,
                      f"Posts default layout should be 'single' or 'post', got '{actual_layout}'")

    def test_author_configured(self):
        self.assertIn("author", self.config, "Missing 'author' block in config")
        author = self.config["author"]
        self.assertIn("name", author, "Missing author.name")
        self.assertIn("bio", author, "Missing author.bio")


class TestPostFrontMatter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.posts = _get_posts()
        cls.front_matters = {}
        for post in cls.posts:
            fm = _parse_front_matter(os.path.join(POSTS_DIR, post))
            cls.front_matters[post] = fm

    def test_posts_exist(self):
        self.assertGreater(len(self.posts), 0, "No posts found")

    def test_all_posts_have_front_matter(self):
        for post, fm in self.front_matters.items():
            self.assertIsNotNone(fm, f"{post}: missing front matter")

    def test_all_posts_have_title(self):
        for post, fm in self.front_matters.items():
            self.assertIn("title", fm, f"{post}: missing title")
            self.assertTrue(len(fm["title"]) > 0, f"{post}: empty title")

    def test_all_posts_have_date(self):
        for post, fm in self.front_matters.items():
            self.assertIn("date", fm, f"{post}: missing date")

    def test_all_posts_have_hidden_true(self):
        for post, fm in self.front_matters.items():
            self.assertTrue(fm.get("hidden", False),
                            f"{post}: expected hidden: true for archived post")

    def test_post_filenames_match_date_format(self):
        pattern = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}-.+\.md$")
        for post in self.posts:
            self.assertRegex(post, pattern, f"{post}: bad filename format")

    def test_no_duplicate_permalinks(self):
        permalinks = {}
        for post, fm in self.front_matters.items():
            link = fm.get("permalink")
            if link:
                self.assertNotIn(link, permalinks,
                                 f"Duplicate permalink '{link}' in {post} and {permalinks.get(link)}")
                permalinks[link] = post


class TestPages(unittest.TestCase):
    EXPECTED_PAGES = {
        "about.md": "/about/",
        "old-articles.md": "/old-articles/",
        "talks.md": "/talks/",
    }

    def test_all_expected_pages_exist(self):
        for page in self.EXPECTED_PAGES:
            path = os.path.join(PAGES_DIR, page)
            self.assertTrue(os.path.isfile(path), f"Missing page: {page}")

    def test_pages_have_permalink(self):
        for page, expected_link in self.EXPECTED_PAGES.items():
            fm = _parse_front_matter(os.path.join(PAGES_DIR, page))
            self.assertIsNotNone(fm, f"{page}: missing front matter")
            self.assertEqual(fm.get("permalink"), expected_link,
                             f"{page}: expected permalink {expected_link}")


class TestTalksData(unittest.TestCase):
    TALKS_FILE = os.path.join(DATA_DIR, "talks.yml")

    def _load_talks(self):
        with open(self.TALKS_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f.read())

    def test_talks_file_exists(self):
        self.assertTrue(os.path.isfile(self.TALKS_FILE), "_data/talks.yml missing")

    def test_talks_has_entries(self):
        talks = self._load_talks()
        self.assertIsInstance(talks, list, "talks.yml must be a list")
        self.assertGreater(len(talks), 0, "talks.yml has no entries")

    def test_talks_entries_have_required_fields(self):
        talks = self._load_talks()
        for talk in talks:
            self.assertIn("title", talk, f"Talk missing 'title': {talk}")
            self.assertIn("event", talk, f"Talk missing 'event': {talk}")


class TestNavigation(unittest.TestCase):
    NAV_FILE = os.path.join(DATA_DIR, "navigation.yml")

    def _load_nav(self):
        with open(self.NAV_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f.read())

    def test_navigation_file_exists(self):
        self.assertTrue(os.path.isfile(self.NAV_FILE), "_data/navigation.yml missing")

    def test_navigation_has_main_list(self):
        nav = self._load_nav()
        self.assertIn("main", nav, "navigation.yml missing 'main' key (Minimal Mistakes format)")
        self.assertIsInstance(nav["main"], list)
        self.assertGreater(len(nav["main"]), 0)

    def test_navigation_url_links_have_matching_pages(self):
        nav = self._load_nav()
        nav_items = nav.get("main", [])
        page_permalinks = set()
        for page_file in os.listdir(PAGES_DIR):
            if page_file.endswith(".md"):
                fm = _parse_front_matter(os.path.join(PAGES_DIR, page_file))
                if fm and "permalink" in fm:
                    page_permalinks.add(fm["permalink"])
        for item in nav_items:
            url = item.get("url")
            if url and not url.startswith("http"):
                normalized = "/" + url.lstrip("/")
                if not normalized.endswith("/"):
                    normalized += "/"
                self.assertIn(normalized, page_permalinks,
                              f"Nav link '{item.get('title')}' -> '{url}' has no matching page")

    def test_navigation_has_old_articles_entry(self):
        nav = self._load_nav()
        urls = [item.get("url", "") for item in nav.get("main", [])]
        self.assertTrue(any("/old-articles" in u for u in urls),
                        "Navigation missing entry for /old-articles/")

    def test_navigation_has_talks_entry(self):
        nav = self._load_nav()
        urls = [item.get("url", "") for item in nav.get("main", [])]
        self.assertTrue(any("/talks" in u for u in urls),
                        "Navigation missing entry for /talks/")


class TestStructure(unittest.TestCase):
    def test_index_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "index.md")), "index.md not found")

    def test_cname_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "CNAME")))

    def test_cname_content(self):
        with open(os.path.join(ROOT, "CNAME"), "r") as f:
            self.assertEqual(f.read().strip(), "blog.unhandledexception.it")

    def test_gemfile_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "Gemfile")))

    def test_gemfile_has_include_cache(self):
        with open(os.path.join(ROOT, "Gemfile"), "r") as f:
            content = f.read()
        self.assertIn("jekyll-include-cache", content,
                      "Gemfile missing jekyll-include-cache — required by Minimal Mistakes")

    def test_no_chirpy_references_in_config(self):
        with open(CONFIG_FILE, "r") as f:
            content = f.read()
        self.assertNotIn("chirpy", content.lower(), "_config.yml still references Chirpy theme")

    def test_no_leftover_tabs_directory(self):
        self.assertFalse(os.path.isdir(os.path.join(ROOT, "_tabs")),
                         "_tabs/ directory should not exist after migration")

    def test_no_leftover_chirpy_layouts(self):
        layouts_dir = os.path.join(ROOT, "_layouts")
        if os.path.isdir(layouts_dir):
            for f in os.listdir(layouts_dir):
                self.fail(f"Unexpected custom layout: _layouts/{f}")

    def test_no_agency_sitetext(self):
        self.assertFalse(os.path.isfile(os.path.join(DATA_DIR, "sitetext.yml")),
                         "_data/sitetext.yml should not exist — Agency theme leftover")

    def test_no_agency_style(self):
        self.assertFalse(os.path.isfile(os.path.join(DATA_DIR, "style.yml")),
                         "_data/style.yml should not exist — Agency theme leftover")


if __name__ == "__main__":
    unittest.main()
