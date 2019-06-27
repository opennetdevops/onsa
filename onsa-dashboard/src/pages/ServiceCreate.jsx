import React from "react";

import {
  onsaServices,
  onsaIrsServices,
  serviceEnum
} from "../site-constants.js";
import { Form, FormRow, FormInput } from "../components/Form";
import FormAlert from "../components/Form/FormAlert";
import FormRadio from "../components/Form/FormRadio";
import  ClientSelect  from "../components/Clients/ClientSelect";

import Select from "react-select";
import { validationSchema} from "../components/Validators/ServiceCreate";

import { URLs, ClientURLs, HTTPGet, HTTPPost } from "../middleware/api.js";
import CustomerLocationModal from '../components/Container/CustomerLocationModal';


class ServiceCreate extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      bandwidth: "",
      clientId: "",
      customerLocId: null,
      custLocationsOptions: [],
      customerLocModal: false,
      dialogLabel: "",
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
      prefix: "29",
      selectedCustLoc: "",
      selectedService: [],
      selectedClient: [],
      servicesOptions: [],
      serviceId: "",
      showPrefix: false,
      showPort: false,
      showMultiPortSwitch: false
    };
  }

  componentDidMount() {
    if (this.state.servicesOptions.length === 0) {
      let options = onsaServices.map(service => {
        return { value: service.type, label: serviceEnum[service.type] };
      });
      this.setState({ servicesOptions: options });
    }

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

  showAlertBox = (result, message, label) => {
    // if there are no arguments, wont show the dialog
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false,
      dialogLabel: label
    });
  };

  resetFormFields = () => {
    this.setState({
      bandwidth: "",
      customerLocId: "",
      multiPortSwitch: false,
      gtsId: "",
      prefix: "29",
      serviceId: "",
      selectedClient: [],
      selectedCustLoc: [],
      selectedLocation: [],
      selectedPortMode: "",
      selectedPort: [],
      selectedService: [],
      showPrefix: false,
      showMultiPortSwitch: false,
      showPort: false
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
    let mpsw = false;

    this.showAlertBox();

    if (value === "new") {
      showPort = false;
    } else {
      if (value === "existing") {
        url = ClientURLs(
          "clientAccessPorts",
          this.state.clientId,
          this.state.customerLocId
        );
        mpsw = false;
      } else if (value === "multi") {
        url = ClientURLs("multiClientPorts");
        mpsw = true;
      }
      this.getAccessPorts(url);
      showPort = true;
    }

    this.setState({
      selectedPortMode: value,
      showPort: showPort,
      showMultiPortSwitch: !showPort,
      multiPortSwitch: mpsw,
      selectedPort: []
    });
  };

  // when existingCPE or Existing-Multi-client is checked.
  getAccessPorts = url => {
    HTTPGet(url).then(
      jsonResponse => {
        let options = jsonResponse.map(port => {
          return {
            value: port.id,
            label: port.access_node + " - " + port.port
          };
        });

        this.setState({
          portOptions: options
        });
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
      selectedPort: selectedOption
    });
  };

  handleClientOnChange = selectedOption => {
    let clientId = "";

    if (selectedOption) {
      clientId = selectedOption.value;
      this.showAlertBox();
      this.getClientLocations(clientId);
    }

    this.setState({
      customerLocId: "",
      selectedCustLoc: "",
      clientId: clientId,
      selectedClient: selectedOption,
      custLocationsOptions: []
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
      selectedPortMode: "new",
      showMultiPortSwitch: true
    });
  };

  handleLocationOnChange = selectedOption => {
    this.setState({ selectedLocation: selectedOption });
  };

  handleServiceTypeOnChange = selectedOption => {
    this.setState({ selectedService: selectedOption }, this.handleDisplays);
  };

  handleDisplays = () => {
    let state = {};
    state = onsaIrsServices.includes(this.state.selectedService.value)
      ? { showPrefix: true }
      : { showPrefix: false };
    this.setState(state);
  };

  handleSubmit = event => {
    event.preventDefault();
    let data = this.getSubmitData();

    let dataToValidate = {
      ...data,
      client: this.state.selectedClient.value,
      custLoc: this.state.selectedCustLoc.value,
      servType: this.state.selectedService.value,
      hub: this.state.selectedLocation.value
    };
    validationSchema()
      .validate(dataToValidate, {
        context: {
          showPort: this.state.showPort,
          showPrefix: this.state.showPrefix
        }
      })
      .then(
        () => {
          //isValid = true
          this.submitRequest(URLs["services"], data);
        }, //isValid = false
        err => {
          this.showAlertBox(false, err.message, "Validation Error: ");
        }
      );
  };

  getSubmitData() {
    let data = {
      client_id: this.state.clientId,
      location_id: this.state.selectedLocation.value,
      id: this.state.serviceId,
      bandwidth: this.state.bandwidth,
      service_type: this.state.selectedService.value,
      customer_location_id: this.state.customerLocId,
      gts_id: this.state.gtsId,
      multiclient_port: this.state.multiPortSwitch
    };

    if (this.state.selectedPort.value) {
      // if CPE already exists
      data["access_port_id"] = this.state.selectedPort.value;
    }
    if (onsaIrsServices.includes(this.state.selectedService.value)) {
      data["prefix"] = this.state.prefix;
    }
    return data;
  }

  submitRequest = (url, data) => {
    HTTPPost(url, data).then(
      () => {
        this.showAlertBox(true, "Service created successfuly");
        this.resetFormFields();
      },
      error => {
        this.showAlertBox(false, error.message);
      }
    );
  };

  handleToggle = (name, value) => {
    this.setState({
      [name]: !value
    });
  };

  handleAddCustomerLocation = event => {
    event.preventDefault();
    this.setState({ customerLocModal: true });
  };

  render() {
    return (
      <React.Fragment>
        <div className="row justify-content-center">
          <div className="col-md-8">
            <FormAlert
              dialogSuccess={this.state.dialogSuccess}
              dialogText={this.state.dialogText}
              dialogShow={this.state.dialogShow}
              msgLabel={this.state.dialogLabel}
            />
          </div>
          <div className="col-md-8 order-md-1">
            <h4>New service</h4>
            <Form className="form" onSubmit={this.handleSubmit}>
              <FormRow className="row">
                {/* client name */}
                <div className="col-lg-6 order-lg-1 mb-3">
                  <label htmlFor="client">Client Name</label>
                  <ClientSelect
                    onChange={this.handleClientOnChange}
                    value={this.state.selectedClient}
                    name="client"
                    searchByMT="3"
                    errorMsg={this.showAlertBox}
                  />
                </div>

                {/* CUST LOC */}
                <div className="col-lg-6 order-lg-3 mb-3">
                  <label htmlFor="customerLoc">Customer Location</label>
                  <sup>
                    <a
                      href="/"
                      onClick={this.handleAddCustomerLocation}
                      className="badge badge-info ml-2 p-1 font-italic "
                      tabIndex="-1"
                    >
                      Add
                    </a>
                  </sup>
                  <Select
                    onChange={this.handleCustLocationOnChange}
                    options={this.state.custLocationsOptions}
                    name="customerLoc"
                    placeholder="Choose one.."
                    value={this.state.selectedCustLoc}
                  />
                </div>

                {/* product id  */}
                <div className="col-lg-6 order-lg-2 mb-3">
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

                {/* GTS ID */}
                <div className="col-lg-6 order-lg-4 mb-3">
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
              <FormRow
                className="row form-row justify-content-center
                                  mx-auto my-2 mb-3 border rounded"
              >
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
              <FormRow className="row ">
                {/* BW */}
                <div className="col-lg-6 mb-3">
                  <label htmlFor="bandwidth">
                    Bandwidth <span className="text-muted"> (In Mbps)</span>
                  </label>
                  <FormInput
                    type="number"
                    min="1"
                    className="form-control "
                    id="bandwidth"
                    name="bandwidth"
                    value={this.state.bandwidth}
                    onChange={this.handleInputChange}
                    placeholder="1024"
                  />
                </div>
                {/* HUB */}
                <div className="col-lg-6 mb-3">
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
              <FormRow className="row ">
                <div className="col-lg-6 mb-3">
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
                  <div className="col-lg-6 mb-3">
                    <label htmlFor="prefix">Prefix</label>
                    <FormInput
                      type="number"
                      min="24"
                      max="32"
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
              {/* MULTIPLE CLIENT PORT SWITCH */}
              {this.state.showMultiPortSwitch && (
                <FormRow className="row form-row mx-auto pr-4">
                  <div className="col-lg-6 p-0  my-2 border rounded ">
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
              {/* SUBMIT BUTTON */}
              <div className="row justify-content-center">
                <div className="col-sm-6 ">
                  <button
                    className="btn btn-primary btn-block btn-lg "
                    type="submit"
                  >
                    Create
                  </button>
                </div>
              </div>
            </Form>
          </div>
        </div>
        <CustomerLocationModal
          isOpen={this.state.customerLocModal}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
          client={this.state.selectedClient}
          getLocations={this.getClientLocations}
          setLocation={this.handleCustLocationOnChange}
        />
      </React.Fragment>
    );
  }
}

export default ServiceCreate;
