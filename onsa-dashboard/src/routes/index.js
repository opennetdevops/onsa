import { Login, Dashboard, ServiceCreate, ServiceModify, Customers, CustomersLocations, ProjectCreate, ProjectAccessPort, ProjectLogicalUnit, ProjectVrf } from '../views';

var publicRoutes = [{ path: "/login", name: "Login", component: Login }];

var privateRoutes = [{ path: "/dashboard", name: "Dashboard", component: Dashboard },
{ path: "/services/create", name: "ServiceCreate", component: ServiceCreate },
{ path: "/services/modify", name: "ServiceModify", component: ServiceModify },
{ path: "/customers", name: "Customers", component: Customers },
{ path: "/customerslocations", name: "CustomersLocations", component: CustomersLocations },
{ path: "/projects/create", name: "ProjectCreate", component: ProjectCreate },
{ path: "/accessports", name: "ProjectAccessPort", component: ProjectAccessPort },
{ path: "/logicalunits", name: "ProjectLogicalUnit", component: ProjectLogicalUnit },
{ path: "/vrfs", name: "ProjectVrf", component: ProjectVrf }];

export { publicRoutes, privateRoutes };
