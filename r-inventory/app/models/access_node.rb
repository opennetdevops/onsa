class AccessNode < ApplicationRecord
	has_many :access_port
    has_and_belongs_to_many :vlan
	belongs_to :location
end
