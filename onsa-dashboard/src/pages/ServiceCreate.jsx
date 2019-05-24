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
  FormInput
} from "../components/Form";
import FormAlert from "../components/Form/FormAlert";
import Select from "react-select";

import { URLs, ClientURLs, HTTPGet, HTTPPost } from "../middleware/api.js";

class ServiceCreate extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      bandwidth: "",
      clientId: "",
      clientName: "",
      clientNetwork:"",
      clientOptions: [],
      cpeExist: false,
      customerLocId: null,
      custLocationsOptions: [],
      displayMessage: "",
      locationsOptions: [],
      selectedLocation: "",
      selectedVRF: "",
      selectedPort:"",
      portsList: [],
      port: "",
      portId: null,
      portOptions:[],
      prefix: "",
      selectedCustLoc: "",
      servicesOptions: [],
      serviceType: "",
      serviceId: "",
      showVrf: false,
      showPrefix: false,
      showClientNetwork: false,
      successAlert: null,
      vrfName: "",
      vrfsOptions: []
    };
  }

  componentDidMount() {
    if (this.state.servicesOptions.length === 0) {
      let options = onsaServices.map(service => {
        return { value: service.type, label: serviceEnum[service.type] };
      });
      this.setState({ servicesOptions: options });
    }

    // Fetch clients
    HTTPGet(URLs["clients"]).then(
      jsonResponse => {
        let options = jsonResponse.map(client => {
          return { value: client.id, label: client.name };
        });
        this.setState({ clientOptions: options });
      },
      error => {
        this.showAlertBox(false, error.message);
        this.setState({ clientOptions: [] });
      }
    );

    // Fetch Locations
    HTTPGet(URLs["locations"]).then(
      jsonResponse => {
        let options = jsonResponse.map(hub => {
          return { value: hub.id, label: hub.name };
        });
        this.setState({ locationsOptions: options });
      },
      error => {
        this.setState({ locationsOptions: [] });
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

  resetFormFields = () => {
    this.setState({
      serviceId: "",
      prexix: "",
      bandwidth: "",
      clientNetwork: ""
    });
  };



  handleInputChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    if (name === "cpeExist") {
      if (event.target.checked) {
        this.getAccessPorts();
      } else {
        this.setState({ cpeExist: false });
      }
    } else {
      this.setState({ [name]: value });
    }
  };

  // when existingCPE is checked.
  getAccessPorts = () => {
    let url = ClientURLs(
      "clientAccessPorts",
      this.state.clientId,
      this.state.customerLocId
    );

    HTTPGet(url).then(
      jsonResponse => {
        let options = jsonResponse.map(port => {
          return { value: port.id, label: port.access_node + " - " + port.access_port };
        });
  
          this.setState({
          portOptions: options,
          cpeExist: true
        });
      },
      error => {
        this.showAlertBox(false, error.message);
        this.setState({
          portOptions: [],
          cpeExist: false
        });
      }
    );
  };

  handlePortOnChange = selectedOption => {
    this.setState({
      selectedPort: selectedOption,
      portId: selectedOption.value

    });
  };

  handleClientOnChange = selectedOption => {
    const clientId = selectedOption.value;
    const clientName = selectedOption.label;

    this.getClientLocations(clientId);
    this.getClientVRFs(clientId);

    this.setState({
      customerLocId: "",
      selectedCustLoc: "",
      clientName: clientName,
      clientId: clientId
    });
  };

  getClientLocations = clientId => {
    //fetch customer location and creates an options array for Select component

    let url = ClientURLs("customerLocations", clientId);

    HTTPGet(url).then(
      jsonResponse => {
        let options = jsonResponse.map(loc => {
          return { value: loc.id, label: loc.address };
        });
        this.setState({ custLocationsOptions: options });
      },
      error => {
        this.setState({ custLocationsOptions: [] });
        this.showAlertBox(false, error.message);
      }
    );
  };

  getClientVRFs = clientId => {
    let url = ClientURLs("clientVRFs", clientId);

    HTTPGet(url).then(
      jsonResponse => {
        let options = jsonResponse.map(vrf => {
          return { value: vrf.id, label: "RT: " + vrf.rt + " - " + vrf.name };
        });
        options.unshift(
          { value: "null", label: "New" },
          { value: "9999", label: "Legacy" }
        );

        this.setState({ vrfsOptions: options });
      },
      error => {
        this.setState({ vrfsOptions: [] });
        this.showAlertBox(false, error.message);
      }
    );
  };

  handleCustLocationOnChange = selectedOption => {
    this.setState({
      customerLocId: selectedOption.value,
      selectedCustLoc: selectedOption
    });
  };

  handleLocationOnChange = selectedOption => {
    this.setState({ selectedLocation: selectedOption });
  };

  handleVRFOnChange = selectedOption => {
    this.setState({
      selectedVRF: selectedOption
    });
  };

  handleServiceTypeOnChange = selectedOption => {
    this.setState(
      { serviceType: selectedOption.value,
        selectedService: selectedOption },
      this.handleDisplays
    );
  };

  handleDisplays = () => {
    let state = {};
    state = onsaVrfServices.includes(this.state.serviceType)
      ? { showVrf: true, showPrefix: false, showClientNetwork: true }
      : { showVrf: false, showPrefix: true , showClientNetwork: false };
    this.setState(state);
    state =
      this.state.serviceType === "vpls" ? { showClientNetwork: false } : null;
    this.setState(state);
  };

  handleSubmit = event => {
    event.preventDefault();

    let data = {
      client_id: this.state.clientId,
      location_id: this.state.selectedLocation.value,
      id: this.state.serviceId,
      bandwidth: this.state.bandwidth,
      service_type: this.state.serviceType,
      customer_location_id: this.state.customerLocId
    };

    if (this.state.portId) {
      // if CPE already exists

      data["prefix"] = this.state.prefix;
      data["access_port_id"] = this.state.portId;

      if (onsaVrfServices.includes(this.state.serviceType)) {
        data["client_network"] = this.state.clientNetwork;
        data["vrf_id"] = this.state.selectedVRF.value;
      }
    } else {
      data["prefix"] = this.state.prefix;

      if (onsaVrfServices.includes(this.state.serviceType)) {
        data["client_network"] = this.state.clientNetwork;
        data["vrf_id"] = this.state.selectedVRF.value;
      }
    }

    HTTPPost(URLs["services"], data).then(
      () => {
        this.showAlertBox(true, "Service created succesfully");
        this.resetFormFields();
      },
      error => {
        this.showAlertBox(false, error.message);
      }
    );
  };

  render() {

    const formIsValid = () => {
      return this.state.serviceId &&
      this.state.selectedCustLoc && 
      this.state.clientId &&
      this.state.bandwidth 
      //this.state.prefix
       ? false 
       : true
    }
    // console.log("form Is valid: ", formIsValid() )

    return (
      <React.Fragment>
        <div className="row justify-content-center">
          <div className="col-md-8">
            <FormAlert
              succesfull={this.state.successAlert}
              displayMessage={this.state.displayMessage}
            />
          </div>
          <div className="col-md-8 order-md-1">
            <FormTitle>New service</FormTitle>
            <Form
              className="needs-validation"
              noValidate
              onSubmit={this.handleSubmit}
            >
              <FormRow className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="client">Client</label>
                  <Select
                    onChange={this.handleClientOnChange}
                    options={this.state.clientOptions}
                    name="client"
                    placeholder="Choose a client.."
                  />

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
                    onChange={this.handleInputChange}
                    required
                  />
                </div>
              </FormRow>

              <FormRow className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="customerLoc">Customer Location</label>
                  <Select
                    onChange={this.handleCustLocationOnChange}
                    options={this.state.custLocationsOptions}
                    name="customerLoc"
                    placeholder="Choose a customer location.."
                    value={this.state.selectedCustLoc}
                    required
                  />
                </div>
              </FormRow>

              <div className="d-block my-3">
                <div className="custom-control custom-radio">
                  <input
                    id="radio"
                    name="cpeExist"
                    type="checkbox"
                    onChange={this.handleInputChange}
                    className="custom-control-input"
                    disabled={!this.state.customerLocId}
                    required
                  />
                  <label className="custom-control-label" htmlFor="radio">
                    Existing CPE
                  </label>
                </div>
              </div>
              {/* PORT */}
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
                  <Select
                    onChange={this.handlePortOnChange}
                    options={this.state.portOptions}
                    name="port"
                    placeholder="Choose a port.."
                    required
                    value={this.state.selectedPort}
                  />
                </div>
              </FormRow>
              {/* PREFIX */}
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
                    min="0"
                    className="form-control"
                    id="bandwidth"
                    name="bandwidth"
                    value={this.state.bandwidth}
                    onChange={this.handleInputChange}
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
                    onChange={this.handleInputChange}
                    placeholder="24"
                    required
                  />
                </div>
              </FormRow>
              {/* SERVICE TYPE */}
              <FormRow className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="serviceType">Service type</label>
                  <Select
                    onChange={this.handleServiceTypeOnChange}
                    options={this.state.servicesOptions}
                    name="serviceType"
                    placeholder="IRS, MPLS, VPLS..."
                    value={this.state.selectedService}
                    required
                  />
                </div>

                <div className="col-md-6 mb-3">
                  <label htmlFor="location">HUB</label>
                  <Select
                    onChange={this.handleLocationOnChange}
                    options={this.state.locationsOptions}
                    name="location"
                    placeholder="Choose a HUB.."
                    value={this.state.selectedLocation}
                    required
                  />
                </div>
              </FormRow>
              {/* VRF */}
              <FormRow className="row">
                <div
                  className="col-md-6 mb-3"
                  style={
                    this.state.showVrf
                      ? { display: "inline" }
                      : { display: "none" }
                  }
                >
                  <label htmlFor="vrfName">VRF</label>
                  <Select
                    onChange={this.handleVRFOnChange}
                    options={this.state.vrfsOptions}
                    name="vrfName"
                    placeholder="Choose the VRF ..."
                    value={this.state.selectedVRF}
                    required
                  />
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
                    onChange={this.handleInputChange}
                    placeholder="192.168.0.0/24"
                    required
                  />
                </div>
              </FormRow>

              <hr className="mb-4" />
              <div className="row justify-content-center">
                <div className="col-md-6 ">
                  <button
                    className="btn btn-primary btn-block btn-lg "
                    disabled= {formIsValid()}
                    // {!this.state.serviceId ? true : false}
                    type="submit"
                  >
                    Create
                  </button>
                </div>
              </div>
            </Form>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default ServiceCreate;
