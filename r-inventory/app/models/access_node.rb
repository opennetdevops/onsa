class AccessNode < ApplicationRecord
	has_many :access_ports
  has_and_belongs_to_many :vlans
	belongs_to :location

	def mgmt_ip
		"#{self[:mgmt_ip].to_s}/#{self[:mgmt_ip].prefix}"
	end

end
