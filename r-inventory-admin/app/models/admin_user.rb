class AdminUser < ApplicationRecord
  # Include default devise modules. Others available are:
  devise :ldap_authenticatable
end
