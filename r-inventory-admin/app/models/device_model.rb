class DeviceModel < ApplicationRecord

	UPLINK_PORTS = ["GigabitEthernet 1/26","GigabitEthernet 1/27"]
	STATUSES = [['Pendiente Config','Pendiente configuración'],['Enviado','Enviado'],['Instalado','Instalado']]

	def to_s
		self.brand + " - " + self.model
	end

end
