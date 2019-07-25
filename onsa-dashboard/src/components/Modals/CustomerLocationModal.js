import React from 'react';
import { Modal, ModalHeader, ModalBody } from "reactstrap";
import CustomerLocation from "../../pages/CustomersLocations"

class CustomerLocationModal extends React.Component {
  
  handleToggle = () => {
    this.props.toggle("customerLocModal", "true");
  };

  componentDidUpdate(){
    // console.log(
    //   "[CustomerLocationModal] DidUpdate"
    // );
  }

  shouldComponentUpdate(nextProps, nextState) {
    let rst = false
    if (nextProps.isOpen !== this.props.isOpen) {
      rst = true
    } 
    return rst
  }

  render() {
    // console.log(
    //   "[CustomerLocationModal] Render!!"
    // );
    return (
      <Modal
        isOpen={this.props.isOpen}
        toggle={this.handleToggle}
        
      >
        <ModalHeader toggle={this.handleToggle}>
        {/* <h4 className="mb-3">Add customer location</h4> */}
        Add customer location
        </ModalHeader>
        <ModalBody>
          <CustomerLocation
            onModal={true}
            selectedClient={this.props.client}
            getLocations={this.props.getLocations}
            modalToggler={this.handleToggle}
            setLocation={this.props.setLocation}
            alert={this.props.alert}
          />

        </ModalBody>
      </Modal>
    );
  }
}

export default CustomerLocationModal;