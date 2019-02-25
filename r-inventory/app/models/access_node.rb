class AccessNode < ApplicationRecord
	has_many :access_ports
    has_and_belongs_to_many :vlans
	belongs_to :location
end
