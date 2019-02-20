class RouterNode < ApplicationRecord
	has_and_belongs_to_many :logical_units
	belongs_to :location
end
