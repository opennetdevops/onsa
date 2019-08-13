import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPPut, HTTPGet } from "../../middleware/api.js";
import classes from "./Modals.module.css";
import Select from "react-select";
import { VALIDATAIONSCHEMA } from "../Validators/ConfigureCPE";
import FormAlert from "../Form/FormAlert";


class TerminateModal extends React.Component {
  state = {
    brands: [],
    dialogShow:false,
    models: [],
    modelsBrands: [],
    ipAddress: "",
    selectedBrand: "",
    selectedModel: "",
    serialNumber: ""
  };

  abortController = new AbortController();

  componentDidMount() {
    HTTPGet(URLs.device_models, this.abortController.signal).then(
      jsonResponse => {
        console.log("original JSON: ", jsonResponse);
        this.mapJsonToArrays(jsonResponse);
      },
      error => {
        if (error.name !== "AbortError") {
          this.props.alert(false, error.message);
        }
      }
    );
  }
  componentDidUpdate(prevProps) {
    if (prevProps.isOpen !== this.props.isOpen) {
      this.setState({ dialogShow: false });
     }
  }


  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({ [name]: value });
  };

  showAlertBox = (result, message, label) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false,
      dialogLabel: label
    });
  };

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
    let data = { service_state: "service_activated" }; // TODO
    const serviceId = this.props.service.id;

    let validateData = {
      ...data,
      serialNumber: this.state.serialNumber,
      ipAddress: this.state.ipAddress,
      brand: this.state.selectedBrand.label,
      model: this.state.selectedModel.label
    };

    VALIDATAIONSCHEMA()
      .validate(validateData)
      .then(
        () => {
          this.props.toggle("terminateModal", "true", serviceId);
          // this.submitRequest( serviceId, data); // TODO validateData
          console.log("SUCCESS GO SUBMIT");
        },
        err => {
          // this.props.alert(false, err.message, "Validation Error: ");
          this.showAlertBox(false, err.message, "Validation Error: ");

          // this.props.toggle("terminateModal", "true");
        }
      );
  };

  submitRequest = (serviceId, data) => {
    HTTPPut(URLs["services"] + "/" + serviceId, data).then(
      () => {
        console.log("[Sended Data]: ", data, "serviceId: ", serviceId);
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

  handleInputChange = event => {
    let name = event.target.name;
    let value = event.target.value;
    this.setState({ [name]: value });
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
          <div className="row justify-content-center">
            <FormAlert
              dialogSuccess={this.state.dialogSuccess}
              dialogText={this.state.dialogText}
              dialogShow={this.state.dialogShow}
              msgLabel={this.state.dialogLabel}
            />
          </div>

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
                  <label htmlFor="serialNumber">CPE S/N</label>
                  <input
                    type="text"
                    name="serialNumber"
                    className="form-control"
                    placeholder="Serial number"
                    value={this.state.serialNumber}
                    onChange={this.handleInputChange}
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="ipAddress"> IP Address </label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="WAN IP address"
                    name="ipAddress"
                    value={this.state.ipAddress}
                    onChange={this.handleInputChange}
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
