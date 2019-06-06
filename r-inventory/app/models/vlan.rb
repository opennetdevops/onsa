class Vlan < ApplicationRecord
	has_and_belongs_to_many :access_node
end
