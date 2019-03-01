class ClientNode < ApplicationRecord
	has_many :client_node_ports

	def mgmt_ip
		"#{self[:mgmt_ip].to_s}/#{self[:mgmt_ip].prefix}"
	end

end
