import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPPut } from "../../middleware/api.js";
import classes from "./Modals.module.css";
import Select from "react-select";

const brands = [
  { value: "Cisco", label: "Cisco" },
  { value: "Transition", label: "Transition" },
  { value: "Huawei", label: "Huawei" }
];

const models = [
  { value: "model1", label: "model1" },
  { value: "model2", label: "model2" },
  { value: "model3", label: "model3" }
];

class TerminateModal extends React.Component {
  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({ [name]: value });
  };

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

  handleToggle = () => {
    this.props.toggle("terminateModal", "true");
  };

  render() {
    const { className } = this.props;

    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        className={className}
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
              {/* <div className="row">
                <div className="col-md-6 mb-3"> */}
                  <div className="form-group row">
                  <label htmlFor="service" className="col-sm-2 col-form-label">Product</label>
                  <div className="col-sm-4">
                  <input
                    type="text"
                    className="form-control"
                    placeholder={this.props.service.id}
                    disabled
                    name="service"
                  />
                  </div>

                  {/* </div>
                </div> */}
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="selectBrand">Brand</label>
                  <Select options={brands} name="selectBrand" />
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="selectModel">Device Model</label>
                  <Select options={models} name="selectModel" />
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
                <label htmlFor="client"> IP Address  </label>
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
