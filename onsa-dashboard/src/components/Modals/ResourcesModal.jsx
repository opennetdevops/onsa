  import React from 'react';
import PropTypes from 'prop-types';

import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Card, CardText, CardBody, CardTitle } from 'reactstrap';


class ResourcesModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modal: false
    }
  }

  handleToggle = () => {
    this.props.toggle("resourcesModal", "false")
  }

  render() {

    const { className, 
            children,
          } = this.props;

    return (
        <Modal isOpen={this.props.isOpen} toggle={this.handleToggle} className={className}>
          <ModalHeader toggle={this.handleToggle}>Resources</ModalHeader>
          <ModalBody>
            <Card className="bg-light">
              <CardBody>
                <CardTitle>Service ID: {this.props.service.id}</CardTitle>                   
                <CardText tag="pre" className="font-weight-light">{children}</CardText>
              </CardBody>
            </Card>
          </ModalBody>
          <ModalFooter>
            <Button color="secondary" onClick={this.handleToggle}>Close</Button>
          </ModalFooter>
        </Modal>
      );
  
  }

  
}

ResourcesModal.propTypes = {
    className: PropTypes.string,
    bsClassName: PropTypes.string
}; 

ResourcesModal.defaultProps = {
  className: "",
};

export default ResourcesModal;