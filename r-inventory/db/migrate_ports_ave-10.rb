sco = AccessNode.where(hostname:"SCO-AVE10").first
24.times do |i| 
	port = AccessPort.create(port:"GigabitEthernet 1/#{i+1}",used:false,multiclient_port:true,access_node_id:sco.id,has_sfp:true)
end