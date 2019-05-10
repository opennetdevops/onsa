class ClientNode < ApplicationRecord
	has_many :client_node_ports
	belongs_to :device_model
	belongs_to :location
	
	def mgmt_ip
		"#{self[:mgmt_ip].to_s}/#{self[:mgmt_ip].prefix}" if self[:mgmt_ip]
	end

end
