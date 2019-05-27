require 'csv'

csv_text = File.read(Rails.root.join('db','hubs-final.csv'), encoding: "utf-8")
csv = CSV.parse(csv_text, :headers => true, :encoding => "utf-8",:col_sep =>",")
csv.each do |row|
  location = Location.new
  location.shortname = row['short_name'] 
  location.name = row['name']
  location.region = row['region']
  location.pop_size = row['pop_size']
  location.save
end
