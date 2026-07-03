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
    def test_index_html_generated(self):
        self.assertTrue(os.path.isfile(os.path.join(SITE_DIR, "index.html")))

    def test_talks_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "talks", "index.html")),
            "Talks page not generated – check _pages/talks.md"
        )

    def test_old_articles_page_generated(self):
        self.assertTrue(
            os.path.isfile(os.path.join(SITE_DIR, "old-articles", "index.html")),
            "Old Articles page not generated – check _pages/old-articles.md"
        )

    def test_sitemap_generated(self):
        self.assertTrue(os.path.isfile(os.path.join(SITE_DIR, "sitemap.xml")))

    def test_feed_generated(self):
        self.assertTrue(os.path.isfile(os.path.join(SITE_DIR, "feed.xml")))


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestHomePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_html = _read_file(os.path.join(SITE_DIR, "index.html"))

    def test_home_does_not_contain_hidden_posts(self):
        hidden_titles = [
            "Singleton in C# thread-safe",
            "Un anno da freelance",
            "Code Contracts in .NET",
            "DevCamp un breve resoconto",
            "Enterprise Library 5",
        ]
        for title in hidden_titles:
            self.assertNotIn(title, self.home_html,
                             f"Hidden post '{title}' should not appear on home page")

    def test_home_has_masthead_nav(self):
        self.assertIn("greedy-nav", self.home_html,
                      "Home page missing Minimal Mistakes masthead/navigation")

    def test_home_has_talks_link(self):
        self.assertIn("/talks/", self.home_html,
                      "Home page should contain link to /talks/")

    def test_home_no_chirpy_leftovers(self):
        chirpy_classes = ["topbar-wrapper", "sidebar-bottom", "#panel-wrapper"]
        for cls in chirpy_classes:
            self.assertNotIn(cls, self.home_html, f"Chirpy leftover found: {cls}")

    def test_home_no_agency_leftovers(self):
        agency_markers = ["agency.scss", "portfolio-modal", "portfolio-hover"]
        for marker in agency_markers:
            self.assertNotIn(marker, self.home_html,
                             f"Agency theme leftover found: {marker}")


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestTalksPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(SITE_DIR, "talks", "index.html")
        cls.html = _read_file(path) if os.path.isfile(path) else ""

    def test_page_not_empty(self):
        self.assertGreater(len(self.html), 0, "Talks page is empty")

    def test_contains_tabia_conf_talk(self):
        self.assertIn("TabIA", self.html, "Talks page should list TabIA Conf talk")


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestOldArticlesPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(SITE_DIR, "old-articles", "index.html")
        cls.html = _read_file(path) if os.path.isfile(path) else ""

    def test_page_not_empty(self):
        self.assertGreater(len(self.html), 0, "Old Articles page is empty")

    def test_contains_archived_post_titles(self):
        expected_titles = [
            "Singleton in C# thread-safe",
            "Un anno da freelance",
            "Enterprise Library 5",
        ]
        for title in expected_titles:
            self.assertIn(title, self.html,
                          f"Old Articles should list '{title}'")

    def test_contains_year_headings(self):
        for year in ["2009", "2010", "2012", "2018"]:
            self.assertIn(year, self.html,
                          f"Old Articles should contain year heading {year}")


@unittest.skipUnless(_site_built(), "_site/ not found – run `bundle exec jekyll build` first")
class TestPostsRendered(unittest.TestCase):
    SAMPLE_POSTS = [
        "2018/07/27/Un-Anno-Da-Freelance-Retrospettiva",
        "2013/10/29/code-contracts-in-net",
    ]

    def test_hidden_posts_still_have_pages(self):
        for post_path in self.SAMPLE_POSTS:
            candidates = [
                os.path.join(SITE_DIR, post_path, "index.html"),
                os.path.join(SITE_DIR, post_path + ".html"),
            ]
            exists = any(os.path.isfile(c) for c in candidates)
            self.assertTrue(exists, f"Post page not generated: {post_path}")


if __name__ == "__main__":
    unittest.main()
