import React from 'react';
import PropTypes from 'prop-types';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

import { onsaIrsServices, onsaVrfServices } from '../../site-constants.js'


async function putJson(url, data) {

    let response = await fetch(url, {
        method: "PUT",
        mode: "cors", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      });

    let jsonResponse = await response.json();

    return jsonResponse;
}

class TerminateModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      serialNumber: ''
    };
  }

  handleChange = (event) => {

    const value = event.target.value;
    const name = event.target.name

    this.setState({[name]: value})
  }

  handleSubmit = (event) => {

    let url = "http://localhost:8000/core/api/services/" + this.props.service.id;

    if (onsaIrsServices.includes(this.props.service.type)) {
      putJson(url, {'service_state': 'service_activated'})
    }
    else if (onsaVrfServices.includes(this.props.service.type)) {
      let data = {'client_node_sn': this.state.serialNumber, 'service_state': 'service_activated'};
      putJson(url, data)
    }    
    
  }

  handleToggle = () => {
    this.props.toggle("terminateModal", "false")
  }

  render() {

    const { className, 
          } = this.props;

    return (
        <Modal isOpen={this.props.isOpen} toggle={this.handleToggle} className={className}>
          <ModalHeader toggle={this.handleToggle}>Terminate service</ModalHeader>
          <ModalBody>                      
                <div className="col-md-12 order-md-1">
                  <form className="needs-validation" noValidate onSubmit={this.handleSubmit}>
                    <div className="row">
                      <div className="col-md-6 mb-3">
                        <label htmlFor="client">Service Id</label>
                        <input type="text" className="form-control" placeholder={this.props.service.id} disabled/>
                      </div>
                      <div className="col-md-6 mb-3" style={ onsaVrfServices.includes(this.props.service.type) ? {display: 'inline'} : {display: 'none'}}>
                        <label htmlFor="clientId">Serial Number</label>
                        <input type="text" className="form-control" id="serialNumber" name="serialNumber" value={this.state.serialNumber} onChange={this.handleChange} placeholder="CCCC3333CCCC" required/>
                      </div>
                    </div> 
                    <ModalFooter>
                      <Button className="btn" type="submit" value="Submit" color="primary" onClick={this.handleToggle}>Continue</Button>
                      <Button color="secondary" onClick={this.handleToggle}>Close</Button>
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
  className: "",
};

export default TerminateModal;