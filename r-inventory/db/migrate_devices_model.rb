require 'csv'
csv_text = File.read(Rails.root.join('db','network-devices.csv'), encoding: "utf-8")
csv = CSV.parse(csv_text, :headers => true, :encoding => "utf-8",:col_sep =>",")
csv.each do |row|
puts row
end