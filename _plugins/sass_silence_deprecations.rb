# frozen_string_literal: true
#
# sass_silence_deprecations.rb
#
# Extends jekyll-sass-converter to pass `silence_deprecations` to Dart Sass,
# enabling the config option in _config.yml under `sass:`:
#
#   sass:
#     silence_deprecations:
#       - import
#       - global-builtin
#       - color-functions
#       - if-function
#       - slash-div
#
# Necessary because jekyll-sass-converter 3.x does not forward
# silence_deprecations to sass-embedded natively.
#
Jekyll::Hooks.register :site, :after_init do |site|
  module Jekyll
    module Converters
      class Scss
        def sass_configs
          config = {
            :load_paths                 => sass_load_paths,
            :charset                    => !associate_page_failed?,
            :source_map                 => sourcemap_required?,
            :source_map_include_sources => true,
            :style                      => sass_style,
            :syntax                     => syntax,
            :url                        => sass_file_url,
            :quiet_deps                 => quiet_deps_option,
            :verbose                    => verbose_option,
          }

          deprecations = Array(jekyll_sass_configuration.fetch("silence_deprecations", []))
          unless deprecations.empty?
            config[:silence_deprecations] = deprecations.map { |d| d.to_s.to_sym }
          end

          config
        end
      end
    end
  end
end
