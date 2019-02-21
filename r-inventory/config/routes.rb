Rails.application.routes.draw do
  resources :router_nodes do 
  	resources :logical_units, only:[:index,:create,:destroy]
  end
  resources :access_nodes
  resources :locations do
  	resources :router_nodes, only:[:index]
  	resources :access_nodes, only:[:index]
  	resources :access_ports, only:[:index]
  end
end
