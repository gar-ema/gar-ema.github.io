"""Tests that validate the generated _site/ after a Jekyll build.

These tests require a successful `bundle exec jekyll build` first.
Run them with: python -m pytest tests/test_build.py -v
"""

import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_DIR = os.path.join(ROOT, "_site")


def _site_built():
    return os.path.isdir(SITE_DIR)


def _read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestBuildOutput(unittest.TestCase):
    """Validate that Jekyll build produced expected output."""

    def test_index_html_generated(self):
        self.assertTrue(os.path.isfile(os.path.join(SITE_DIR, "index.html")))

    def test_about_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "about", "index.html"))
        )

    def test_categories_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "categories", "index.html"))
        )

    def test_tags_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "tags", "index.html"))
        )

    def test_archives_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "archives", "index.html"))
        )

    def test_old_articles_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "old-articles", "index.html")),
            "Old Articles page not generated – check _pages/old-articles.md and include: [_pages] in _config.yml"
        )

    def test_sitemap_generated(self):
        self.assertTrue(os.path.isfile(os.path.join(SITE_DIR, "sitemap.xml")))

    def test_feed_generated(self):
        self.assertTrue(os.path.isfile(os.path.join(SITE_DIR, "feed.xml")))


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestHomePage(unittest.TestCase):
    """Validate that the home page does not show hidden posts."""

    @classmethod
    def setUpClass(cls):
        cls.home_html = _read_file(os.path.join(SITE_DIR, "index.html"))

    def test_home_does_not_contain_hidden_posts(self):
        # These are titles of known hidden/archived posts
        hidden_titles = [
            "Singleton in C# thread-safe",
            "Un anno da freelance",
            "Code Contracts in .NET",
            "DevCamp un breve resoconto",
            "Enterprise Library 5",
        ]
        for title in hidden_titles:
            self.assertNotIn(
                title, self.home_html,
                f"Hidden post '{title}' should not appear on home page"
            )

    def test_home_has_no_post_entries(self):
        """Currently all posts are hidden, so the home should have no entries."""
        # MM uses class 'archive__item' for post entries in the home layout
        count = self.home_html.count("archive__item")
        self.assertEqual(count, 0,
                         f"Home page should show 0 posts, found {count} entries")


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestOldArticlesPage(unittest.TestCase):
    """Validate that Old Articles page lists the archived posts."""

    @classmethod
    def setUpClass(cls):
        path = os.path.join(SITE_DIR, "old-articles", "index.html")
        if os.path.isfile(path):
            cls.html = _read_file(path)
        else:
            cls.html = ""

    def test_page_not_empty(self):
        self.assertGreater(len(self.html), 0, "Old Articles page is empty")

    def test_contains_archived_post_titles(self):
        expected_titles = [
            "Singleton in C# thread-safe",
            "Un anno da freelance",
            "Enterprise Library 5",
        ]
        for title in expected_titles:
            self.assertIn(
                title, self.html,
                f"Old Articles should list '{title}'"
            )

    def test_contains_year_headings(self):
        # Note: 2008 file has date: 2009-11-02 in front matter, so it's under 2009
        for year in ["2009", "2010", "2012", "2018"]:
            self.assertIn(year, self.html,
                          f"Old Articles should contain year heading {year}")


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestPostsRendered(unittest.TestCase):
    """Validate that individual post pages are still generated (even if hidden from home)."""

    # Permalinks without trailing slash generate .html files directly
    SAMPLE_POSTS = [
        "2018/07/27/Un-Anno-Da-Freelance-Retrospettiva",
        "2013/10/29/code-contracts-in-net",
    ]

    def test_hidden_posts_still_have_pages(self):
        for post_path in self.SAMPLE_POSTS:
            candidates = [
                os.path.join(SITE_DIR, post_path, "index.html"),
                os.path.join(SITE_DIR, post_path + ".html"),
                os.path.join(SITE_DIR, "posts",
                             post_path.split("/")[-1], "index.html"),
            ]
            exists = any(os.path.isfile(c) for c in candidates)
            self.assertTrue(exists,
                            f"Post page not generated: {post_path}")


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestNoChirpyLeftovers(unittest.TestCase):
    """Ensure no Chirpy-specific markup leaked into the build."""

    def test_no_chirpy_css_classes_on_home(self):
        html = _read_file(os.path.join(SITE_DIR, "index.html"))
        chirpy_classes = ["topbar-wrapper", "sidebar-bottom", "#panel-wrapper"]
        for cls in chirpy_classes:
            self.assertNotIn(cls, html,
                             f"Chirpy leftover found: {cls}")


if __name__ == "__main__":
    unittest.main()
