import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPPut, HTTPGet } from "../../middleware/api.js";
import classes from "./Modals.module.css";
import Select from "react-select";

class TerminateModal extends React.Component {
  state = {
    brands: [],
    models: [],
    modelsBrands: [],
    selectedBrand: null,
    selectedModel: null
  };

  abortController = new AbortController();

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({ [name]: value });
  };

  componentDidMount() {
    HTTPGet(URLs.device_models, this.abortController.signal).then(
      jsonResponse => {
        // console.log("original JSON: ", jsonResponse);
        this.mapJsonToArrays(jsonResponse);
      },
      error => {
        if (error.name !== "AbortError") {
          this.props.alert(false, error.message);
        }
      }
    );
  }
  componentWillUnmount() {
    this.abortController.abort();
  }

  mapJsonToArrays = devicesJson => {
    let brands = [];
    let modelsBrands = [];

    if (devicesJson.length) {
      devicesJson.forEach(device => {
        brands.push({ value: device.brand, label: device.brand });

        modelsBrands.push({ brand: device.brand, model: device.model });
      });
      const distinctBrands = this.getDistinctValues(brands);

      brands = distinctBrands.map(brand => ({ value: brand, label: brand }));
    }
    this.setState({ modelsBrands: modelsBrands, brands: brands });
  };

  getDistinctValues = array => [...new Set(array.map(x => x.value))];

  handleSubmit = () => {
    let data = { service_state: "service_activated" };
    const serviceId = this.props.service.id;

    this.props.toggle("terminateModal", "true", serviceId);

    HTTPPut(URLs["services"] + "/" + serviceId, data).then(
      () => {
        this.props.serviceHasChanged(serviceId, "terminateServ");
      },
      error => {
        this.props.onUpdateError(error.message, serviceId);
      }
    );
  };

  handleSelectBrandChange = selectedOption => {
    let models = [];
    this.state.modelsBrands.forEach(item => {
      if (item.brand === selectedOption.value) {
        models.push({ value: item.model, label: item.model });
      }
    });
    this.setState({ selectedBrand: selectedOption, models: models });
  };
  handleSelectModelChange = selectedOption =>
    this.setState({ selectedModel: selectedOption });

  handleToggle = () => {
    this.props.toggle("terminateModal", "true");
  };

  render() {
    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        returnFocusAfterClose={false}
        contentClassName={classes.ActionsModal}
      >
        <ModalHeader
          toggle={this.handleToggle}
          className={classes.ActionsModalHeader}
        >
          Configure CPE
        </ModalHeader>
        <ModalBody>
          <div className="col-md-12 order-md-1">
            <form>
              <div className="form-group row">
                <label htmlFor="service" className="col-sm-2 col-form-label">
                  Product
                </label>
                <div className="col-sm-4">
                  <input
                    type="text"
                    className="form-control"
                    placeholder={this.props.service.id}
                    disabled
                    name="service"
                  />
                </div>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="selectBrand">Brand</label>
                  <Select
                    options={this.state.brands}
                    name="selectBrand"
                    onChange={this.handleSelectBrandChange}
                    value={this.state.selectedBrand}
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="selectModel">Device Model</label>
                  <Select
                    options={this.state.models}
                    name="selectModel"
                    onChange={this.handleSelectModelChange}
                    value={this.state.selectedModel}
                  />
                </div>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="client">CPE S/N</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Serial number"
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="client"> IP Address </label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="WAN IP address"
                  />
                </div>
              </div>

              <ModalFooter className={classes.ActionsModalFooter}>
                <Button
                  className="btn"
                  color="primary"
                  onClick={this.handleSubmit}
                >
                  Continue
                </Button>
                <Button color="secondary" onClick={this.handleToggle}>
                  Close
                </Button>
              </ModalFooter>
            </form>
          </div>
        </ModalBody>
      </Modal>
    );
  }
}

TerminateModal.propTypes = {
  className: PropTypes.string,
  bsClassName: PropTypes.string,
  alert: PropTypes.func
};

TerminateModal.defaultProps = {
  className: ""
};

export default TerminateModal;
