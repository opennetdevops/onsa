Rails.application.routes.draw do
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)
  scope 'inventory/api' do
      post '/authenticate', to: 'authentication#authenticate'
    resources :router_nodes do 
    	resources :logical_units, only:[:index,:create,:destroy]
    end
    resources :client_nodes do
      resources :client_node_ports
    end
    resources :access_nodes do 
      resources :access_ports
      resources :vlans, only:[:index,:create,:destroy]
    end
    resources :locations do
      resources :vrfs
      resources :router_nodes, only:[:index]
      resources :access_nodes, only:[:index]
      resources :access_ports, only:[:index]
    end
    resources :vlans, only:[:index,:create,:destroy]
    resources :vrfs
    resources :access_ports
    resources :logical_units, only:[:index,:create,:destroy]
    resources :contracts, only:[:show]
    resources :device_models, only:[:index,:show]

  end
end
