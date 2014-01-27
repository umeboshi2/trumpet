require 'jekyll_asset_pipeline'


module JekyllAssetPipeline
    class CoffeeScriptConverter < JekyllAssetPipeline::Converter
      require 'coffee-script'

      def self.filetype
        '.coffee'
      end

      def convert
        return CoffeeScript.compile(@content)
      end
    end
end

module JekyllAssetPipeline
  class SassConverter < JekyllAssetPipeline::Converter
    require 'sass'

    def self.filetype
      '.scss'
    end

    def convert
      return Sass::Engine.new(@content, syntax: :scss).render
    end
  end
end
