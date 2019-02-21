class AccessNode < ApplicationRecord
	has_many :access_port
	belongs_to :location
end
