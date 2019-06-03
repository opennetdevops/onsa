import React from "react";
import { Button, Badge } from "reactstrap";
import {
  serviceEnum,
  serviceStatesEnum,
  onsaIrsServices,
  onsaVrfServices
} from "../site-constants.js";
import {
  ResourcesModal,
  ActivateModal,
  AccessNodeModal,
  TerminateModal,
  UnsubscribeModal
} from "../components/Modals";

import FormAlert from "../components/Form/FormAlert";
import { URLs, HTTPGet } from "../middleware/api.js";

class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      activateModal: false,
      accessNodeActivateModal: false,
      successAlert: null,
      displayMessage: "",
      modalService: { id: null, type: null },
      resources: null,
      resourcesModal: false,
      services: [],
      terminateModal: false
    };
  }

  componentDidMount() {

    HTTPGet(URLs["services"]).then(
      jsonResponse => this.setState({ services: jsonResponse }),
      error => this.showAlertBox(false, error.message)
    );

    this.props.displayNavbar(false);
  }

  showAlertBox = (result, message) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: ( message || result) ? true : false
    });
  };

  handleOnClick = event => {
    const value = event.target.value;
    const name = event.target.name;

    let service = JSON.parse(value);

    switch (name) {
      case "resources":
        let url =
          process.env.REACT_APP_CORE_URL +
          "/core/api/services/" +
          service.id +
          "/resources";

        HTTPGet(url).then(
          jsonResponse => {
            this.setState({
              resources: jsonResponse,
              resourcesModal: !this.state.resourcesModal,
              modalService: { id: service.id, type: service.service_type }
            });
          },
          error => {
            this.showAlertBox(false, error.message);
          }
        ); //todo

        break;
      case "activate":
        this.setState({
          activateModal: !this.state.accessNodeActivateModal,
          modalService: { id: service.id, type: service.service_type }
        });
        break;
      case "anActivate":
        this.setState({
          accessNodeActivateModal: !this.state.accessNodeActivateModal,
          modalService: { id: service.id, type: service.service_type }
        });
        break;
      case "terminate":
        this.setState({
          terminateModal: !this.state.terminateModal,
          modalService: { id: service.id, type: service.service_type }
        });
        break;
      case "unsubscribe":
        this.setState({
          unsubsModal: !this.state.unsubsModal,
          modalService: { id: service.id, type: service.service_type }
        });
        break;
      default:
        break;
    }
  };

  handleToggle = (name, value) => {
    this.setState({ [name]: !value });
  };

  render() {
    const tableRows = this.state.services.map(service => {
      return (
        <tr className="table-borderless" key={service.id}>
          <td>
            <Badge color="primary">{service.id}</Badge>
          </td>
          <td>
            <Badge color="secondary">{service.gts_id}</Badge>
          </td>
          <td>
            <Badge color="success">{serviceEnum[service.service_type]}</Badge>
          </td>
          <td>
            <Badge color="secondary">
              {serviceStatesEnum[service.service_state]}
            </Badge>
          </td>
          <td>
            <Button
              className="btn btn-primary btn-sm btn-block"
              color="primary"
              name="resources"
              onClick={this.handleOnClick}
              type="button"
              value={JSON.stringify(service)}
            >
              View details
            </Button>
          </td>
          {service.service_state === "in_construction" &&
          onsaVrfServices.includes(service.service_type) ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="success"
                name="anActivate"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
              >
                Configure SCO
              </Button>
            </td>
          ) : null}
          {service.service_state === "in_construction" &&
          onsaIrsServices.includes(service.service_type) ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="success"
                name="activate"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
              >
                Activate
              </Button>
            </td>
          ) : null}
          {(service.service_state === "an_activated" &&
            onsaVrfServices.includes(service.service_type)) ||
          (service.service_state === "cpe_data_ack" &&
            onsaIrsServices.includes(service.service_type)) ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="info"
                name="terminate"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
              >
                Terminate
              </Button>
            </td>
          ) : null}
          <td>
            <Button
              className="btn btn-primary btn-sm btn-block"
              color="danger"
              name="unsubscribe"
              onClick={this.handleOnClick}
              type="button"
              value={service.id}
            >
              Unsubscribe
            </Button>
          </td>
        </tr>
      );
    });

    return (
      <div className="container-fluid">
        <div className="row justify-content-center">
          <FormAlert
           dialogSuccess={this.state.dialogSuccess}
           dialogText={this.state.dialogText}
           dialogShow={this.state.dialogShow}
          />
        </div>
        <div className="row">
          <table className="table table-hover col-md-12">
            <thead>
              <tr>
                <th scope="col">Product ID</th>
                <th scope="col">GTS </th>
                <th scope="col">Service Type</th>
                <th scope="col">Service State</th>
              </tr>
            </thead>
            <tbody>{tableRows}</tbody>
          </table>
        </div>

        <ResourcesModal
          isOpen={this.state.resourcesModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        >
          {JSON.stringify(this.state.resources, null, 2)}
        </ResourcesModal>
        <ActivateModal
          isOpen={this.state.activateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        />
        <AccessNodeModal
          isOpen={this.state.accessNodeActivateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        />
        <TerminateModal
          isOpen={this.state.terminateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        />
        <UnsubscribeModal
          isOpen={this.state.unsubsModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        />
      </div>
    );
  }
}

export default Dashboard;
