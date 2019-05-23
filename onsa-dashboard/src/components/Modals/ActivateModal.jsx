import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPPost } from "../../middleware/api.js";

class ActivateModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      serialNumber: ""
    };
  }

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleSubmit = event => {
    const data = {
      cpe_sn: this.state.serialNumber,
      deployment_mode: "automated",
      target_state: "cpe_data_ack"
    };

    HTTPPost(
      URLs["services"] + "/" + this.props.service.id + "/activation",
      data
    );
  };

  handleToggle = () => {
    this.props.toggle("activateModal", "false");
  };

  render() {
    const { className } = this.props;

    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        className={className}
      >
        <ModalHeader toggle={this.handleToggle}>Activate service</ModalHeader>
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
                <div className="col-md-6 mb-3">
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

ActivateModal.propTypes = {
  className: PropTypes.string,
  bsClassName: PropTypes.string
};

ActivateModal.defaultProps = {
  className: ""
};

export default ActivateModal;
