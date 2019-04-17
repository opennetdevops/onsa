class Location < ApplicationRecord
	has_many :access_nodes
	has_many :router_nodes
	has_many :client_nodes
	has_and_belongs_to_many :vrfs
end
