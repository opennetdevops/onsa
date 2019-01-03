	import { Login, Dashboard, ServiceCreate, ServiceModify, Customers, CustomersLocations } from '../views';

var indexRoutes = [
  { path: "/login", name: "Login", component: Login },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/services/create", name: "ServiceCreate", component: ServiceCreate },
  { path: "/services/modify", name: "ServiceModify", component: ServiceModify },
  { path: "/customers", name: "Customers", component: Customers },
  { path: "/customerslocations", name: "CustomersLocations", component: CustomersLocations },
];

export default indexRoutes;
