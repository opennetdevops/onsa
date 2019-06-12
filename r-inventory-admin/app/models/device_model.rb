class DeviceModel < ApplicationRecord

	STATUSES = [['Pendiente Config','Pendiente configuración'],['Enviado','Enviado'],['Instalado','Instalado']]

	def to_s
		self.brand + " - " + self.model
	end

	def uplink_ports_array
		if self.uplink_ports
			self.uplink_ports.split(',')
		else
			[]
		end
	end

end
