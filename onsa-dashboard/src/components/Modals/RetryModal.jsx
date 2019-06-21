import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPPut } from "../../middleware/api.js";

class RetryModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = { confirmed: false };
  }

  handleRetry = () => {
    let serviceId = this.props.service.id;

    //URL DE PRUEBA!!
    HTTPPut(URLs["services"] + "/" + serviceId).then(
      () => {
        this.props.toggle("retryModal", "true", "retry");
        this.props.alert(true, "The service with product ID " + serviceId + ", has been \"updated\".");
      },
      error => {
        // this.props.alert(false, error.message)
        // this.props.toggle("retryModal", "true");
        this.props.toggle("retryModal", "true", "retry"); // INVERTIR CON LINEA ANTERIOR CUANDO LA URL SEA CORRECTA
      }
    );
  };

  handleToggle = () => {
    this.props.toggle("retryModal", "true");
  };

  handleInputChange = event => {
    this.setState({ confirmed : event.target.checked });
  };

  render() {
    const { className } = this.props;

    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        className={className}
      >
        <ModalHeader toggle={this.handleToggle}>Retry</ModalHeader>
        <ModalBody>
          <div className="col-md-12 order-md-1">
            <form
              className="needs-validation"
              noValidate
              onSubmit={this.handleSubmit}
            >
              <div className="col-md-6 mb-1">
                
              </div>
              <div className="col-md-8 mb-1 mt-5 mb-5">
                <div className="custom-control custom-checkbox">
                  <input
                    type="checkbox"
                    className="custom-control-input"
                    id="confirmCheck"
                    onChange={this.handleInputChange}
                    value={this.state.confirmed}
                  />
                  <label
                    className="custom-control-label muted"
                    htmlFor="confirmCheck"
                  >
                    Check this to confirm the action.
                  </label>
                </div>
              </div>

              <ModalFooter>
                <Button
                  className="btn btn-primary"
                  onClick={this.handleRetry}
                  disabled={!this.state.confirmed}
                  color="primary"
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

RetryModal.propTypes = {
  className: PropTypes.string,
  bsClassName: PropTypes.string,
  alert: PropTypes.func

};

RetryModal.defaultProps = {
  className: ""
};

export default RetryModal;
