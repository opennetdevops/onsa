Rails.application.routes.draw do
  resources :router_nodes do 
  	resources :logical_units, only:[:index,:create,:destroy]
  end
  resources :client_nodes do
    resources :client_ports
  end
  resources :access_nodes do 
    resources :vlan_tags, only:[:index,:create,:destroy]
  end
  resources :locations do
    resources :vrfs
    resources :router_nodes, only:[:index]
    resources :access_nodes, only:[:index]
    resources :access_ports, only:[:index]
  end
  resources :vlan_tags, only:[:index,:create,:destroy]
  resources :vrfs
  resources :access_ports
  resources :logical_units, only:[:index,:create,:destroy]
end
