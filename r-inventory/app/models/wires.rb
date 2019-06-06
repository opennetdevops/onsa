class Wires < ApplicationRecord
    belongs_to :vlan
    belongs_to :access_node
end
