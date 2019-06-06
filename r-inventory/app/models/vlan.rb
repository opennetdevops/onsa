class Vlan < ApplicationRecord
	has_many :wires
	has_many :access_nodes, through: :wires
end
