class Contract < ApplicationRecord
	has_many :access_nodes

	def to_s
		self.provider + " - " + self.number
	end
end
