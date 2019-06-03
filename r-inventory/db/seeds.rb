if Rails.env.development?
    files = Dir["db/seeds/local/*.json"].sort
    files.each do |a|
        json = ActiveSupport::JSON.decode(File.read(a))
        file_name = File.basename(a, ".*").sub /^\w+-/, ''
        json.each do |b|
            c = Object.const_get(file_name.singularize.camelcase).new(b)
            c.save(validate: false)
        end
    end
end



