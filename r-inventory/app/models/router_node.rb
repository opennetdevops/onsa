class RouterNode < ApplicationRecord
	has_and_belongs_to_many :logical_units
	belongs_to :location
	belongs_to :device_model
	belongs_to :contract, optional:true
	has_many :distribution_nodes, foreign_key: 'remote_device_id'

	def mgmt_ip
		"#{self[:mgmt_ip].to_s}/#{self[:mgmt_ip].prefix}" if self[:mgmt_ip]
	end

	def private_wan_ip
		"#{self[:private_wan_ip].to_s}/#{self[:private_wan_ip].prefix}" if self[:private_wan_ip]
	end

	def loopback
		"#{self[:loopback].to_s}/#{self[:loopback].prefix}" if self[:loopback]
	end

	def to_s
		self.hostname
	end

end
