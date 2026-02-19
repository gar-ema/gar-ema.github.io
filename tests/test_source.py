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
    """Extract YAML front matter from a file."""
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
    return sorted(
        f for f in os.listdir(POSTS_DIR) if f.endswith(".md")
    )


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------

class TestConfig(unittest.TestCase):
    """Validate _config.yml structure."""

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

    def test_has_required_fields(self):
        for field in ["title", "description", "url", "author", "plugins"]:
            self.assertIn(field, self.config, f"Missing field: {field}")

    def test_plugins_include_required(self):
        plugins = self.config["plugins"]
        for p in ["jekyll-paginate", "jekyll-sitemap", "jekyll-feed",
                   "jekyll-seo-tag"]:
            self.assertIn(p, plugins, f"Missing plugin: {p}")

    def test_pagination_configured(self):
        self.assertIn("paginate", self.config)
        self.assertIsInstance(self.config["paginate"], int)
        self.assertGreater(self.config["paginate"], 0)

    def test_includes_pages_directory(self):
        """_pages dir must be in 'include' or Jekyll ignores it (causes 404)."""
        includes = self.config.get("include", [])
        self.assertIn("_pages", includes,
                      "Missing include: [_pages] – pages will 404")

    def test_defaults_set_layout(self):
        defaults = self.config.get("defaults", [])
        post_defaults = [
            d for d in defaults
            if d.get("scope", {}).get("type") == "posts"
        ]
        self.assertTrue(len(post_defaults) > 0, "No defaults for posts")
        self.assertIn("layout", post_defaults[0]["values"])


# ---------------------------------------------------------------------------
# Post front matter tests
# ---------------------------------------------------------------------------

class TestPostFrontMatter(unittest.TestCase):
    """Validate that all posts have correct front matter."""

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
        """All current posts should be hidden (archived). New posts should
        NOT have hidden: true, so update this test when adding new content."""
        for post, fm in self.front_matters.items():
            self.assertTrue(
                fm.get("hidden", False),
                f"{post}: expected hidden: true for archived post"
            )

    def test_post_filenames_match_date_format(self):
        pattern = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}-.+\.md$")
        for post in self.posts:
            self.assertRegex(post, pattern, f"{post}: bad filename format")

    def test_no_duplicate_permalinks(self):
        permalinks = {}
        for post, fm in self.front_matters.items():
            link = fm.get("permalink")
            if link:
                self.assertNotIn(
                    link, permalinks,
                    f"Duplicate permalink '{link}' in {post} and {permalinks.get(link)}"
                )
                permalinks[link] = post


# ---------------------------------------------------------------------------
# Pages tests
# ---------------------------------------------------------------------------

class TestPages(unittest.TestCase):
    """Validate that all expected pages exist."""

    EXPECTED_PAGES = {
        "about.md": "/about/",
        "archive.md": "/archives/",
        "categories.md": "/categories/",
        "tags.md": "/tags/",
        "old-articles.md": "/old-articles/",
    }

    def test_all_expected_pages_exist(self):
        for page in self.EXPECTED_PAGES:
            path = os.path.join(PAGES_DIR, page)
            self.assertTrue(os.path.isfile(path), f"Missing page: {page}")

    def test_pages_have_permalink(self):
        for page, expected_link in self.EXPECTED_PAGES.items():
            fm = _parse_front_matter(os.path.join(PAGES_DIR, page))
            self.assertIsNotNone(fm, f"{page}: missing front matter")
            self.assertEqual(
                fm.get("permalink"), expected_link,
                f"{page}: expected permalink {expected_link}"
            )


# ---------------------------------------------------------------------------
# Navigation tests
# ---------------------------------------------------------------------------

class TestNavigation(unittest.TestCase):
    """Validate navigation.yml links correspond to actual pages."""

    def test_navigation_file_exists(self):
        path = os.path.join(DATA_DIR, "navigation.yml")
        self.assertTrue(os.path.isfile(path))

    def test_navigation_links_have_matching_pages(self):
        with open(os.path.join(DATA_DIR, "navigation.yml"), "r") as f:
            nav = yaml.safe_load(f.read())

        page_permalinks = set()
        for page_file in os.listdir(PAGES_DIR):
            if page_file.endswith(".md"):
                fm = _parse_front_matter(os.path.join(PAGES_DIR, page_file))
                if fm and "permalink" in fm:
                    page_permalinks.add(fm["permalink"])

        for item in nav.get("main", []):
            self.assertIn(
                item["url"], page_permalinks,
                f"Nav link '{item['title']}' -> '{item['url']}' has no matching page"
            )

    def test_navigation_has_required_entries(self):
        with open(os.path.join(DATA_DIR, "navigation.yml"), "r") as f:
            nav = yaml.safe_load(f.read())

        urls = [item["url"] for item in nav.get("main", [])]
        for required in ["/categories/", "/tags/", "/about/", "/old-articles/"]:
            self.assertIn(required, urls, f"Missing nav entry for {required}")


# ---------------------------------------------------------------------------
# Structural tests
# ---------------------------------------------------------------------------

class TestStructure(unittest.TestCase):
    """Validate project structure."""

    def test_index_html_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "index.html")))

    def test_cname_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "CNAME")))

    def test_cname_content(self):
        with open(os.path.join(ROOT, "CNAME"), "r") as f:
            self.assertEqual(f.read().strip(), "blog.unhandledexception.it")

    def test_gemfile_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "Gemfile")))

    def test_no_chirpy_references_in_config(self):
        with open(CONFIG_FILE, "r") as f:
            content = f.read()
        self.assertNotIn("chirpy", content.lower(),
                         "_config.yml still references Chirpy theme")

    def test_no_leftover_tabs_directory(self):
        self.assertFalse(
            os.path.isdir(os.path.join(ROOT, "_tabs")),
            "_tabs/ directory should not exist after migration"
        )

    def test_no_leftover_chirpy_layouts(self):
        layouts_dir = os.path.join(ROOT, "_layouts")
        if os.path.isdir(layouts_dir):
            for f in os.listdir(layouts_dir):
                self.fail(f"Unexpected custom layout: _layouts/{f}")


if __name__ == "__main__":
    unittest.main()
