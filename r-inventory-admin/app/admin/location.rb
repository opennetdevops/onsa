ActiveAdmin.register Location do

  controller do
    def permitted_params
      params.permit!
    end
  end

  filter :name
  filter :shortname
  filter :address
  filter :pop_sieze
  filter :region
  
end
