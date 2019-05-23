class AccessNode < ApplicationRecord
	has_many :access_ports
  	has_and_belongs_to_many :vlans
	belongs_to :location
	belongs_to :device_model
	belongs_to :contract,  optional:true
	belongs_to :remote_device, class_name: 'DistributionNode', optional:true

	def mgmt_ip
		"#{self[:mgmt_ip].to_s}/#{self[:mgmt_ip].prefix}" if self[:mgmt_ip]
	end

end
