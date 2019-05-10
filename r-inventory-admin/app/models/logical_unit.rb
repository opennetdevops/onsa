class LogicalUnit < ApplicationRecord
	has_and_belongs_to_many :router_nodes
end
