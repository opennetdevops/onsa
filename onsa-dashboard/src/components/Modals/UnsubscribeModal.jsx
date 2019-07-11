import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPDelete } from "../../middleware/api.js";

class UnsubscribeModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = { confirmed: false };
  }
  
  componentDidUpdate(prevProps) {
    if (prevProps.isOpen !== this.props.isOpen) {
      this.setState({ confirmed: false });
    }
  }

  handleUnsubscribe = () => {
    let serviceId = this.props.service.id;
    let prevState = this.props.service.prevServState
    let operationStatus =  null

    this.props.toggle("unsubscribeModal", "true", serviceId)

    HTTPDelete(URLs["services"] + "/" + serviceId).then(
      (response) => {

        if (prevState === "in_construction") {
          operationStatus = "unsubscribeCompleted";
        } else {
          operationStatus = "unsubscribeInProgress";
          this.props.alert(
            "info",
            "The service with product ID " +
              serviceId +
              " is being updated..."
          );
        }
        this.props.serviceHasChanged(serviceId, operationStatus);
      },
      error => {
        this.props.onUpdateError(error.message, serviceId)
      }
    );
  };

  handleToggle = () => {
    this.props.toggle("unsubscribeModal", "true");
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
        <ModalHeader toggle={this.handleToggle}>Unsubscribe</ModalHeader>
        <ModalBody>
          <div className="col-md-12 order-md-1">
            <form >
              <div className="col-md-6 mb-1">
                <label htmlFor="client">Product Id</label>

                <input
                  type="text"
                  id="client"
                  className="form-control"
                  placeholder={this.props.service.id}
                  disabled
                />
              </div>
              <div className="col-md-8 mb-1 mt-2">
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
                  onClick={this.handleUnsubscribe}
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

UnsubscribeModal.propTypes = {
  className: PropTypes.string,
  bsClassName: PropTypes.string,
  alert: PropTypes.func
};

UnsubscribeModal.defaultProps = {
  className: ""
};

export default UnsubscribeModal;
