class ClientNode < ApplicationRecord
	has_many :client_node_ports
	belongs_to :location
end
