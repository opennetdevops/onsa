import React from 'react';
import PropTypes from 'prop-types';

import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class AccessNodeModal extends React.Component {
  // handleChange = (event) => {

  //   const value = event.target.value;
  //   const name = event.target.name

  //   console.log(value)

  //   this.setState({[name]: value})
  // }

  handleSubmit = (event) => {
    const data = { 'deployment_mode': 'automated', 'target_state': 'an_activated' };

    fetch("http://localhost:8000/core/api/services/" + this.props.service.id + "/activation",
      {
        method: "POST",
        mode: "cors", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(myJson => console.log(myJson))
  }

  handleToggle = () => {
    this.props.toggle("accessNodeActivateModal", "true")
  }

  render() {

    const { className, 
          } = this.props;

    return (
        <Modal isOpen={this.props.isOpen} toggle={this.handleToggle} className={className}>
          <ModalHeader toggle={this.handleToggle}>Activate SCO</ModalHeader>
          <ModalBody>                      
                <div className="col-md-12 order-md-1">
                  <form className="needs-validation" noValidate onSubmit={this.handleSubmit}>
                    <div className="row">
                      <div className="col-md-12 mb-3">
                        <label htmlFor="client">Service Id</label>
                        <input type="text" className="form-control" placeholder={this.props.service.id} disabled/>
                      </div>
                    </div> 
                    <ModalFooter>
                      <Button className="btn" type="submit" value="Submit" color="primary" onClick={this.handleToggle}>Activate</Button>
                      <Button color="secondary" onClick={this.handleToggle}>Close</Button>
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
    bsClassName: PropTypes.string
}; 

AccessNodeModal.defaultProps = {
  className: "",
};

export default AccessNodeModal;