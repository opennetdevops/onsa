import React from "react";
import PropTypes from "prop-types";
import { URLs, HTTPPost } from "../../middleware/api.js";

import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

class AccessNodeModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      vlanId: ""
    };
  }

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleSubmit = () => {
    let data = {};
    const serviceId = this.props.service.id

    if (this.props.service.type === "tip") {
      data = {
        deployment_mode: "automated",
        target_state: "an_activated",
        vlan_id: this.state.vlanId
      };
    } else {
      data = {
        deployment_mode: "automated",
        target_state: "an_activated"
      };
    }
    HTTPPost(URLs["services"] + "/" + serviceId + "/activation", data)
    .then( () => {
        this.props.alert(
          true,
          "The service with product ID " + serviceId + " has been updated."
        );
        console.log("data param: ", data , "serviceId: ", serviceId )
        this.props.toggle("accessNodeActivateModal", "true", "configSCO");
      },

      error => {
        this.props.alert(false, error.message);
        this.props.toggle("accessNodeActivateModal", "true");
      }
    );
  };

  handleToggle = () => {
    this.props.toggle("accessNodeActivateModal", "true");
  };

  render() {
    const { className } = this.props;

    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        className={className}
      >
        <ModalHeader toggle={this.handleToggle}>Activate SCO</ModalHeader>
        <ModalBody>
          <div className="col-md-12 order-md-1">
            <form >
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="client">Service Id</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder={this.props.service.id}
                    disabled
                  />
                </div>

                {this.props.service.type === "tip" ? (
                  <div className="col-md-6 mb-3">
                    <label htmlFor="clientId">Vlan ID</label>
                    <input
                      type="text"
                      className="form-control"
                      id="vlanId"
                      name="vlanId"
                      value={this.state.vlanId}
                      onChange={this.handleChange}
                      placeholder="1 - 4094"
                      required
                    />
                  </div>
                ) : null}
              </div>
              <ModalFooter>
                <Button
                  className="btn"
                  // type="submit"
                  // value="Submit"
                  color="primary"
                  onClick={this.handleSubmit}
                >
                  Activate
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

AccessNodeModal.propTypes = {
  className: PropTypes.string,
  bsClassName: PropTypes.string,
  alert: PropTypes.func
};

AccessNodeModal.defaultProps = {
  className: ""
};

export default AccessNodeModal;
