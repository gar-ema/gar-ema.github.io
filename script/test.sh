#!/bin/bash
set -e

echo "=== Source validation tests ==="
python3 -m pytest tests/test_source.py -v

echo ""
echo "=== Building site ==="
bundle exec jekyll build
echo "Build OK"

echo ""
echo "=== Build output tests ==="
python3 -m pytest tests/test_build.py -v

echo ""
echo "All tests passed!"
