class DeviceModel < ApplicationRecord

	def to_s
		self.brand + " - " + self.model
	end

end
