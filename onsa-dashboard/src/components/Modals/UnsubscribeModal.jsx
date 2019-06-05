import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { URLs, HTTPDelete } from "../../middleware/api.js";

class UnsubscribeModal extends React.Component {
  handleSubmit = () => {
    HTTPDelete(URLs["services"] + "/" + this.props.service.id)
      .then(response => response.json())
      .then(myJson => console.log(myJson));
  };

  handleToggle = () => {
    this.props.toggle("unsubscribeModal", "true");
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
            <form
              className="needs-validation"
              noValidate
              onSubmit={this.handleSubmit}
            >
              <div className="col-md-6 mb-3">
                <label htmlFor="client">Service Id</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder={this.props.service.id}
                  disabled
                />
              </div>
              {/* <p>
                Are you sure you want to teardown this service
                {this.props.service.id}?
              </p> */}
              <ModalFooter>
                <Button
                  className="btn"
                  type="submit"
                  value="Submit"
                  color="danger"
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

UnsubscribeModal.propTypes = {
  className: PropTypes.string,
  bsClassName: PropTypes.string
};

UnsubscribeModal.defaultProps = {
  className: ""
};

export default UnsubscribeModal;
