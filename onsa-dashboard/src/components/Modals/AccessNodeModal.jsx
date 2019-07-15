import React from "react";
import PropTypes from "prop-types";
import { URLs, HTTPPost } from "../../middleware/api.js";

import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { validationSchema } from "../../components/Validators/ConfigureSCO" ;



class AccessNodeModal extends React.Component { 
  constructor(props) {
    super(props);
     // create a ref to store the button DOM element
     this.inputVlan = React.createRef();

    this.state = {
      vlanId: "",
    };
  }  
  
  componentDidUpdate(prevProps) {
    if (prevProps.isOpen !== this.props.isOpen) {
      this.setState({ vlanId: "" });
      //  if (this.props.service.type === "tip") {
      //  this.inputVlan.current.focus();
      // console.log(this.inputVlan)
      // }
     }
  }


  handleChange = event => {
    const value = event.target.value;
    const name = event.target.name;

    this.setState({ [name]: value });
  };

  handleSubmit = () => {
    let data = {};

    const serviceId = this.props.service.id;
    let vlanInput = null

    if (this.props.service.type === "tip") {
      vlanInput = this.state.vlanId
      data = {
        deployment_mode: "automated",
        target_state: "an_activated",
        vlan_id: vlanInput
      };
   
    } else {
      data = {
        deployment_mode: "automated",
        target_state: "an_activated"
      };
    }

    let validateData  = { vlanId: vlanInput }
    
    validationSchema()
      .validate( validateData )
        .then(
          () => {
            this.props.toggle("accessNodeActivateModal", "true", serviceId)
            this.submitRequest( serviceId, data);
          }, 
          err => {
            this.props.alert(false, err.message, "Validation Error: ");
            this.props.toggle("accessNodeActivateModal", "true");
          }
        );
  };

  submitRequest = ( serviceId, data ) => {
    
    HTTPPost(URLs["services"] + "/" + serviceId + "/activation", data).then(
      response => {
        this.props.alert(
          "info",
          "The service with product ID " + serviceId + " is being updated..."
        );
        console.log("[Sended Data]: ", data, "serviceId: ", serviceId);
        console.log("[Post Response] : ", response);

        this.props.serviceHasChanged(serviceId,"configSCO");
      },

      error => {
        this.props.onUpdateError(error.message, serviceId);
      }
    );
  }

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
        returnFocusAfterClose={false}
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
                      type="number"
                      className="form-control"
                      id="vlanId"
                      name="vlanId"
                      value={this.state.vlanId}
                      onChange={this.handleChange}
                      placeholder="1 - 4094"
                      ref={this.inputVlan} 
                    />
                  </div>
                ) : null}
              </div>
              <ModalFooter>
                <Button
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
