class DistributionNode < ApplicationRecord
	belongs_to :location
	belongs_to :device_model
	belongs_to :contract, optional:true
	belongs_to :remote_device, class_name: 'RouterNode', optional:true
	has_many :access_nodes, foreign_key: 'remote_device_id'

	def to_s
		self.hostname
	end
end
