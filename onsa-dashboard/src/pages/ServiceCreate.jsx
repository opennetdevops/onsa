import React from "react";

import {
  onsaServices,
  onsaIrsServices,
  serviceEnum
} from "../site-constants.js";
import { Form, FormRow, FormTitle, FormInput  } from "../components/Form";
import FormAlert from "../components/Form/FormAlert";
import FormRadio from "../components/Form/FormRadio";

import Select from "react-select";

import { URLs, ClientURLs, HTTPGet, HTTPPost } from "../middleware/api.js";

class ServiceCreate extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      bandwidth: "",
      clientId: "",
      clientName: "",
      clientOptions: [],
      customerLocId: null,
      custLocationsOptions: [],
      dialogSuccess: false,
      dialogText: "",
      dialogShow: false,
      gtsId: "",
      multiPortSwitch: false,
      locationsOptions: [],
      selectedLocation: "",
      selectedPort: "",
      selectedPortMode: null,
      portsList: [],
      portId: null,
      portOptions: [],
      portModeSelection: [
        { label: "New", value: "new" },
        { label: "Existing CPE", value: "existing" },
        { label: "Existing multiple client", value: "multi" }
      ],
      prefix: "",
      selectedCustLoc: "",
      servicesOptions: [],
      serviceType: "",
      serviceId: "",
      showPrefix: false,
      showPort: false

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
    // if there are no arguments, wont show the dialog
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false
    });
  };

  resetFormFields = () => {
    this.setState({
      serviceId: "",
      prexix: "",
      bandwidth: ""
    });
  };

  handleInputChange = event => {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({ [name]: value });

    if (name === "multiPortSwitch") { 
      this.setState({ [name]: event.target.checked });
    }
  };

  handlePortModeChange = event => {
    const value = event.target.value;
    let showPort = false;
    let url = "";

    if (value === "new") {
      showPort = false;
    } else {
      if (value === "existing") {
        url = ClientURLs(
          "clientAccessPorts",
          this.state.clientId,
          this.state.customerLocId
        );
      } else if (value === "multi") {
        // TODO DEFINE NEW URL
        url = ClientURLs("multiClientPorts")
      }
      this.getAccessPorts(url);
      showPort = true;
    }

    this.setState({
      selectedPortMode: value,
      showPort: showPort
    });
  };

  // when existingCPE or Existing-Multi-client is checked.
  getAccessPorts = url => {
    HTTPGet(url).then(
      jsonResponse => {
        let options = jsonResponse.map(port => {
          return {
            value: port.id,
            label: port.access_node + " - " + port.access_port
          };
        });

        this.setState({
          portOptions: options
        });
        this.showAlertBox();
      },
      error => {
        this.showAlertBox(false, error.message);
        this.setState({
          portOptions: []
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

    this.showAlertBox();
    this.getClientLocations(clientId);

    this.setState({
      customerLocId: "",
      selectedCustLoc: "",
      clientName: clientName,
      clientId: clientId
    });
  };

  getClientLocations = clientId => {
    //fetch customer location 
    //creates an options array for Select component

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

  handleCustLocationOnChange = selectedOption => {
    this.setState({
      customerLocId: selectedOption.value,
      selectedCustLoc: selectedOption,
      selectedPortMode: "new"
    });
  };

  handleLocationOnChange = selectedOption => {
    this.setState({ selectedLocation: selectedOption });
  };

  handleServiceTypeOnChange = selectedOption => {
    this.setState(
      { serviceType: selectedOption.value, selectedService: selectedOption },
      this.handleDisplays
    );
  };

  handleDisplays = () => {
    let state = {};
    state = onsaIrsServices.includes(this.state.serviceType)
      ? { showPrefix: true }
      : { showPrefix: false };
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
      customer_location_id: this.state.customerLocId,
      gts_id: this.state.gtsId,
      multiclient_port: this.state.multiPortSwitch
    };

    if (this.state.portId) {
      // if CPE already exists
      data["access_port_id"] = this.state.portId;
    }
    if (onsaIrsServices.includes(this.state.serviceType)) {
      data["prefix"] = this.state.prefix;
    }
   
    HTTPPost(URLs["services"], data).then(
      () => {
        this.showAlertBox(true, "Service created successfuly");
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
        ? //this.state.prefix
          false
        : true;
    };

    return (
      <React.Fragment>
        <div className="row justify-content-center">
          <div className="col-md-8">
            <FormAlert
              dialogSuccess={this.state.dialogSuccess}
              dialogText={this.state.dialogText}
              dialogShow={this.state.dialogShow}
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
                  />
                </div>
              </FormRow>

              <FormRow className="row ">
                {/* CUST LOC */}
                <div className="col-md-6 mb-3">
                  <label htmlFor="customerLoc">Customer Location</label>
                  <Select
                    onChange={this.handleCustLocationOnChange}
                    options={this.state.custLocationsOptions}
                    name="customerLoc"
                    placeholder="Choose a customer location.."
                    value={this.state.selectedCustLoc}
                  />
                </div>
                {/* GTS ID */}
                <div className="col-md-6 mb-3">
                  <label htmlFor="gtsId">GTS ID</label>
                  <FormInput
                    type="text"
                    className="form-control"
                    placeholder="GTS Id"
                    name="gtsId"
                    value={this.state.gtsId}
                    onChange={this.handleInputChange}
                  />
                </div>
              </FormRow>

              {/* PORT MODE */}
              <FormRow className="row form-row justify-content-center mx-auto my-2 border rounded">
                <div className="col-auto m-2 ">
                  {this.state.portModeSelection.map((portMode, index) => {
                    return (
                      <FormRadio
                        id={portMode.value}
                        groupName="portModeSelection"
                        onChange={event => this.handlePortModeChange(event)}
                        value={portMode.value}
                        selectedOption={this.state.selectedPortMode}
                        disabled={!this.state.customerLocId}
                        label={portMode.label}
                        key={index}
                      />
                    );
                  })}
                </div>
              </FormRow>

              {/* PORT */}
              {this.state.showPort && this.state.customerLocId && (
                <FormRow className="row">
                  <div className="col-md-12 mb-3">
                    <label htmlFor="port">Port</label>
                    <Select
                      onChange={this.handlePortOnChange}
                      options={this.state.portOptions}
                      name="port"
                      placeholder="Choose a port.."
                      value={this.state.selectedPort}
                    />
                  </div>
                </FormRow>
              )}
              <FormRow className="row">
                {/* BW */}
                <div className="col-md-6 mb-3">
                  <label htmlFor="bandwidth">
                    Bandwidth <span className="text-muted"> (In Mbps)</span>
                  </label>
                  <FormInput
                    type="number"
                    min="0"
                    className="form-control "
                    id="bandwidth"
                    name="bandwidth"
                    value={this.state.bandwidth}
                    onChange={this.handleInputChange}
                    placeholder="100"
                  />
                </div>
                {/* HUB */}
                <div className="col-md-6 mb-3">
                  <label htmlFor="location">HUB</label>
                  <Select
                    onChange={this.handleLocationOnChange}
                    options={this.state.locationsOptions}
                    name="location"
                    placeholder="Choose a HUB.."
                    value={this.state.selectedLocation}
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
                  />
                </div>
                {/* PREFIX */}
                {this.state.showPrefix && (
                  <div className="col-md-6 mb-3">
                    <label htmlFor="prefix">Prefix</label>
                    <FormInput
                      type="number"
                      className="form-control"
                      id="prefix"
                      name="prefix"
                      value={this.state.prefix}
                      onChange={this.handleInputChange}
                      placeholder="24"
                    />
                  </div>
                )}
              </FormRow>
              {/* MULTIPLE CLIENT PORT */}
              {!this.state.showPort && (
                <FormRow className="row form-row mx-auto pr-4">
                  <div className="col-6 p-0  my-2 border rounded ">
                    <div className="custom-control custom-switch  m-2">
                      <input
                        type="checkbox"
                        className="custom-control-input"
                        name="multiPortSwitch"
                        onChange={this.handleInputChange}
                        value={this.state.multiPortSwitch}
                        id="multiPortSwitch"
                      />
                      <label
                        className="custom-control-label"
                        htmlFor="multiPortSwitch"
                      >
                        Multiple clients port
                      </label>
                    </div>
                  </div>
                </FormRow>
              )}

              <hr className="mb-4" />
              <div className="row justify-content-center">
                <div className="col-md-6 ">
                  <button
                    className="btn btn-primary btn-block btn-lg "
                    disabled={formIsValid()}
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
