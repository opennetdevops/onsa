class ManageAuthorization < ActiveAdmin::AuthorizationAdapter

  def authorized?(action, subject = nil)
    ActiveDirectory.connect 
    case subject
    when normalized(AccessNode)
      if action == :update || action == :destroy || action == :create
        if ActiveDirectory.connection_ok?
          ActiveDirectory.admins.include?(user.email)
        else
          false
        end
      else
        true
      end
    else
      true
    end
  end

end