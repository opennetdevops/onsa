class BackboneNode < ApplicationRecord
	belongs_to :location
	belongs_to :device_model
	belongs_to :contract
end
