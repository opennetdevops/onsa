import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPPut } from "../../middleware/api.js";

import {
  onsaIrsServices,
  onsaVrfServices,
  onsaExternalVlanServices
} from "../../site-constants.js";

class TerminateModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      serialNumber: "",
      vlanId: ""
    };
  }

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({ [name]: value });
  };

  handleSubmit = event => {
    let data = { service_state: "service_activated" };

    if (
      onsaIrsServices.includes(this.props.service.type) ||
      onsaVrfServices.includes(this.props.service.type)
    ) {
      HTTPPut(URLs["services"] + "/" + this.props.service.id, data);
    } else if (onsaExternalVlanServices.includes(this.props.service.type)) {
      let data = {
        vlan_id: this.state.vlanId,
        service_state: "service_activated"
      };
      HTTPPut(URLs["services"] + "/" + this.props.service.id, data);
    }
  };

  handleToggle = () => {
    this.props.toggle("terminateModal", "false");
  };

  render() {
    const { className } = this.props;

    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        className={className}
      >
        <ModalHeader toggle={this.handleToggle}>Terminate service</ModalHeader>
        <ModalBody>
          <div className="col-md-12 order-md-1">
            <form
              className="needs-validation"
              noValidate
              onSubmit={this.handleSubmit}
            >
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
                {/* <div
                  className="col-md-4 mb-3"
                  style={
                    onsaVrfServices.includes(this.props.service.type)
                      ? { display: "inline" }
                      : { display: "none" }
                  }
                >
                  <label htmlFor="clientId">Serial Number</label>
                  <input
                    type="text"
                    className="form-control"
                    id="serialNumber"
                    name="serialNumber"
                    value={this.state.serialNumber}
                    onChange={this.handleChange}
                    placeholder="CCCC3333CCCC"
                    required
                  />
                </div> */}
                <div
                  className="col-md-6 mb-3"
                  style={
                    onsaExternalVlanServices.includes(this.props.service.type)
                      ? { display: "inline" }
                      : { display: "none" }
                  }
                >
                  <label htmlFor="clientId">Serial Number</label>
                  <input
                    type="text"
                    className="form-control"
                    id="vlanId"
                    name="vlanId"
                    value={this.state.vlanId}
                    onChange={this.handleChange}
                    placeholder="<Vlan Id from 1 to 4096>"
                    required
                  />
                </div>
              </div>
              <ModalFooter>
                <Button
                  className="btn"
                  type="submit"
                  value="Submit"
                  color="primary"
                  onClick={this.handleToggle}
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
  bsClassName: PropTypes.string
};

TerminateModal.defaultProps = {
  className: ""
};

export default TerminateModal;
