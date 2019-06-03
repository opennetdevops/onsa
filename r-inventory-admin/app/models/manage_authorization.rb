class ManageAuthorization < ActiveAdmin::AuthorizationAdapter

  def authorized?(action, subject = nil)
    ActiveDirectory.connect 
    if action == :update || action == :destroy || action == :create
        ActiveDirectory.admins.include?(user.email)
    else
      true
    end
  end

end