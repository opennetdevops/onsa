import React from "react";
import PropTypes from "prop-types";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

async function deleteJson(url) {
  let response = await fetch(url, {
    method: "DELETE",
    mode: "cors",
    headers: {
      "Content-Type": "application/json"
    }
  });

  let jsonResponse = await response.json();

  return jsonResponse;
}

class UnsubscribeModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      serviceId: ""
    };
  }

  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleSubmit = event => {
    let url =
      process.env.REACT_APP_CORE_URL +
      "/core/api/services/" +
      this.props.service.id;
    deleteJson(url);
  };

  handleToggle = () => {
    this.props.toggle("unsubsModal", "false");
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
              {/*                      <div className="col-md-6 mb-3">
                        <label htmlFor="client">Service Id</label>
                        <input type="text" className="form-control" placeholder={this.props.serviceId} disabled/>
                      </div>*/}
              <p>Are you sure you want to teardown this service?</p>
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
