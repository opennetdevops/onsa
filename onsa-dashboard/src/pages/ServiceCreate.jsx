import React from "react";

import {
  onsaServices,
  onsaVrfServices,
  serviceEnum
} from "../site-constants.js";
import {
  Form,
  FormRow,
  FormTitle,
  FormInput,
  FormSelect
} from "../components/Form";
import FormAlert from "../components/Form/FormAlert";

import { URLs, HTTPGet, HTTPPost } from "../middleware/api.js";


class ServiceCreate extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      token: "",
      clients: [],
      vrfs: [],
      locations: [],
      location: "",
      portsList: [],
      port: "",
      portId: null,
      customerLocations: [],
      customerLoc: "",
      customerLocId: null,
      client: "",
      clientId: "",
      serviceType: "",
      bandwidth: "",
      prefix: "",
      serviceId: "",
      vrfName: "",
      cpeExist: false,
      modal: false,
      showVrf: false,
      showPrefix: false,
      showClientNetwork: false,
      successAlert: null,
      displayMessage: ""
    };
  }

  componentDidMount() {

    // Fetch clients
    HTTPGet(URLs["clients"]).then(
      jsonResponse => {
        this.setState({ clients: jsonResponse });
      },
      error => {
        this.setState({ clients: [] });
        this.showAlertBox(false, error.message);
      }
    );

    // Fetch Locations
    HTTPGet(URLs["locations"]).then(
      jsonResponse => {
        this.setState({ locations: jsonResponse });
      },
      error => {
        this.setState({ locations: [] });
        this.showAlertBox(false, error.message);
      }
    );

    this.props.displayNavbar(false);
  }

  showAlertBox = (result, message) => {
    this.setState({
      successAlert: result,
      displayMessage: message
    });
  };

  handleDisplays = () => {
    let state = {};
    state = onsaVrfServices.includes(this.state.serviceType)
      ? { showVrf: true, showPrefix: false, showClientNetwork: true }
      : { showClientNetwork: false, showVrf: false, showPrefix: true };
    this.setState(state);
    state =
      this.state.serviceType === "vpls" ? { showClientNetwork: false } : null;
    this.setState(state);
  };

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    switch (name) {
      case "cpeExist":
        this.setState({ [name]: !this.state.cpeExist });

        if (this.state.client && this.state.customerLocId) {
          let url =
            "http://" +
            process.env.REACT_APP_SERVER_IP +
            ":8000/core/api/clients/" +
            this.state.clientId +
            "/customerlocations/" +
            this.state.customerLocId +
            "/accessports";
        
          HTTPGet(url).then(
            jsonResponse => {
              this.setState({ portsList: jsonResponse });
            },
            error => {
              this.showAlertBox(false, error.message);
              this.setState({ portsList: [] });
            }
          );
        }

        break;
      default:
        this.setState({ [name]: value });
    }
  };

  handleOnSelect = event => {
    const value = event.target.value;
    const name = event.target.name;
    let id = event.target.options.selectedIndex;

    if (id === 0) {
      id = null;
    }

    switch (name) {
      case "client":
        this.setState({ [name]: value }, this.handleClient);
        break;
      case "customerLoc":
        this.setState({ [name]: value, customerLocId: id });
        break;
      case "port":
        this.setState({ [name]: value, portId: id });
        break;
      case "serviceType":
        this.setState({ [name]: value }, this.handleDisplays);
        break;
      default:
        this.setState({ [name]: value });
    }

    switch (value) {
      case "new":
        this.setState({ modal: true, vrfName: "" });
        break;
      default:
        break;
    }
  };

  resetFormFields = () => {
    this.setState({
      serviceId: "",
      prexix: "",
      bandwidth: "",
      clientNetwork: ""
    });
  };

  handleSubmit = event => {
    event.preventDefault();

    let data = {};

    if (this.state.portId) {
      data = {
        client: this.state.client,
        location: this.state.location,
        id: this.state.serviceId,
        bandwidth: this.state.bandwidth,
        prefix: this.state.prefix,
        service_type: this.state.serviceType,
        customer_location_id: this.state.customerLocId,
        access_port_id: this.state.portId
      };
      if (onsaVrfServices.includes(this.state.serviceType)) {
        data = {
          client: this.state.client,
          location: this.state.location,
          id: this.state.serviceId,
          bandwidth: this.state.bandwidth,
          service_type: this.state.serviceType,
          client_network: this.state.clientNetwork,
          customer_location_id: this.state.customerLocId,
          access_port_id: this.state.portId
        };
      }
    } else {
      data = {
        client: this.state.client,
        location: this.state.location,
        id: this.state.serviceId,
        bandwidth: this.state.bandwidth,
        prefix: this.state.prefix,
        service_type: this.state.serviceType,
        customer_location_id: this.state.customerLocId
      };
      if (onsaVrfServices.includes(this.state.serviceType)) {
        data = {
          client: this.state.client,
          location: this.state.location,
          id: this.state.serviceId,
          bandwidth: this.state.bandwidth,
          service_type: this.state.serviceType,
          client_network: this.state.clientNetwork,
          customer_location_id: this.state.customerLocId
        };
      }
    }

    HTTPPost(URLs["services"], data).then(
      () => {
        this.showAlertBox(true, "Service created succesfully");
        this.resetFormFields();
      },
      error => {
        console.error("error debug: ", error.message);
        this.showAlertBox(false, error.message);
      }
    );

  };

  handleToggle = event => {
    if (event.target.id === "cancel") {
      this.setState({ vrfName: "" });
    }

    this.setState({
      modal: !this.state.modal
    });
  };

  handleClient = () => {
    //  handler Select  Client
    if (this.state.client !== "") {
      let url =
        "http://" +
        process.env.REACT_APP_SERVER_IP +
        ":8000/core/api/vrfs?client=" +
        this.state.client;

      HTTPGet(url).then(jsonResponse => {
        this.state.client !== "Choose..."
          ? this.setState({ vrfs: jsonResponse })
          : this.setState({ vrfs: [] });
      });

      url =
        "http://" +
        process.env.REACT_APP_SERVER_IP +
        ":8000/core/api/clients?name=" +
        this.state.client;

      HTTPGet(url)
        .then(client => {
          this.state.client !== "Choose..."
            ? this.setState({ clientId: client.id })
            : this.setState({ clientId: "" });
        })
        .then(() => {
          url =
            "http://" +
            process.env.REACT_APP_SERVER_IP +
            ":8000/core/api/clients/" +
            this.state.clientId +
            "/customerlocations";

          HTTPGet(url).then(jsonResponse => {
            this.state.client !== "Choose..."
              ? this.setState({ customerLocations: jsonResponse })
              : this.setState({ customerLocations: [] });
          });
        });
    } else {
      this.setState({ clientId: null });
    }
  };

  createVrfElements = () => {
    if (this.state.vrfs.length > 0) {
      return this.state.vrfs.map(vrf => (
        <option key={vrf.rt} value={vrf.name}>
          {vrf.name}
        </option>
      ));
    } else {
      return [];
    }
  };

  createCustLocsList = () => {
    if (this.state.customerLocations.length > 0) {
      return this.state.customerLocations.map(loc => (
        <option key={loc.id} value={loc.address}>
          {loc.address}
        </option>
      ));
    } else {
      return [];
    }
  };

  render() {
    const clientsList = this.state.clients.map(client => (
      <option key={client.id} value={client.name}>
        {client.name}
      </option>
    ));
    const serviceList = onsaServices.map(service => (
      <option key={service.id} value={service.type}>
        {serviceEnum[service.type]}
      </option>
    ));
    const locationsList = this.state.locations.map(location => (
      <option key={location.id} value={location.name}>
        {location.name}
      </option>
    ));
    const portsList = this.state.portsList.map(port => (
      <option key={port.id} value={port.access_port}>
        {port.access_node + " - " + port.access_port}
      </option>
    ));
    let vrfList = this.createVrfElements();
    let customerLocsList = this.createCustLocsList();

    return (
      <React.Fragment>
        <div className="col-md-8">
          <FormAlert
            succesfull={this.state.successAlert}
            displayMessage={this.state.displayMessage}
          />
        </div>
        <div className="col-md-6 order-md-1">
          <FormTitle>New service</FormTitle>
          <Form
            className="needs-validation"
            noValidate
            onSubmit={this.handleSubmit}
          >
            <FormRow className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="client">Client</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="client"
                  name="client"
                  value={this.state.client}
                  // defaultValue={this.state.client}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {clientsList}
                </FormSelect>
                <div className="invalid-feedback">
                  Example invalid feedback text
                </div>
              </div>

              <div className="col-md-6 mb-3">
                <label htmlFor="serviceId">Product ID</label>
                <FormInput
                  type="text"
                  className="form-control"
                  id="serviceId"
                  placeholder="Id"
                  name="serviceId"
                  value={this.state.serviceId}
                  onChange={this.handleChange}
                  required
                />
              </div>
            </FormRow>

            <FormRow className="row">
              <div className="col-md-12 mb-3">
                <label htmlFor="customerLoc">Customer Location</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="customerLoc"
                  name="customerLoc"
                  value={this.state.customerLoc}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {customerLocsList}
                </FormSelect>
              </div>
            </FormRow>

            <div className="d-block my-3">
              <div className="custom-control custom-radio">
                <input
                  id="radio"
                  name="cpeExist"
                  type="checkbox"
                  onChange={this.handleChange}
                  className="custom-control-input"
                  disabled={!this.state.customerLocId}
                  required
                />
                <label className="custom-control-label" htmlFor="radio">
                  Existing CPE
                </label>
              </div>
            </div>

            <FormRow className="row">
              <div
                className="col-md-12 mb-3"
                style={
                  this.state.cpeExist && this.state.customerLocId
                    ? { display: "inline" }
                    : { display: "none" }
                }
              >
                <label htmlFor="port">Port</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="port"
                  name="port"
                  value={this.state.port}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {portsList}
                </FormSelect>
              </div>
            </FormRow>

            <FormRow className="row">
              <div
                className={
                  this.state.showPrefix ? "col-md-6 mb-3" : "col-md-6 mb-3"
                }
              >
                <label htmlFor="prefix">
                  Bandwidth <span className="text-muted"> (In Mbps)</span>
                </label>
                <FormInput
                  type="number"
                  className="form-control"
                  id="bandwidth"
                  name="bandwidth"
                  value={this.state.bandwidth}
                  onChange={this.handleChange}
                  placeholder="100"
                  required
                />
              </div>

              <div
                className="col-md-6 mb-3"
                style={
                  this.state.showPrefix
                    ? { display: "inline" }
                    : { display: "none" }
                }
              >
                <label htmlFor="prefix">Prefix</label>
                <FormInput
                  type="number"
                  className="form-control"
                  id="prefix"
                  name="prefix"
                  value={this.state.prefix}
                  onChange={this.handleChange}
                  placeholder="24"
                  required
                />
              </div>
            </FormRow>

            <FormRow className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="serviceType">Service type</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="serviceType"
                  name="serviceType"
                  value={this.state.serviceType}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {serviceList}
                </FormSelect>
              </div>

              <div className="col-md-6 mb-3">
                <label htmlFor="location">HUB</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="location"
                  name="location"
                  value={this.state.location}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option value="">Choose...</option>
                  {locationsList}
                </FormSelect>
              </div>
            </FormRow>

            <FormRow className="row">
              <div
                className="col-md-6 mb-3"
                style={
                  this.state.showVrf
                    ? { display: "inline" }
                    : { display: "none" }
                }
              >
                <label htmlFor="prefix">VRF</label>
                <FormSelect
                  className="custom-select d-block w-100"
                  id="vrfName"
                  name="vrfName"
                  value={this.state.vrfName}
                  onChange={this.handleOnSelect}
                  required
                >
                  <option defaultValue value="new">
                    New
                  </option>
                  {vrfList.length ? vrfList : null}
                </FormSelect>
              </div>

              <div
                className="col-md-6 mb-3"
                style={
                  this.state.showClientNetwork
                    ? { display: "inline" }
                    : { display: "none" }
                }
              >
                <label htmlFor="clientNetwork">Client network</label>
                <FormInput
                  type="text"
                  className="form-control"
                  id="clientNetwork"
                  name="clientNetwork"
                  value={this.state.clientNetwork}
                  onChange={this.handleChange}
                  placeholder="192.168.0.0/24"
                  required
                />
              </div>
            </FormRow>

            <hr className="mb-4" />
            <button
              className="btn btn-primary btn-lg btn-block"
              disabled={!this.state.serviceId ? true : false}
              type="submit"
            >
              Create
            </button>
          </Form>
        </div>
      </React.Fragment>
    );
  }
}

export default ServiceCreate;
