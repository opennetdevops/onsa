import React from "react";
import { Button, Badge } from "reactstrap";
import {
  serviceEnum,
  serviceStatesEnum,
  onsaIrsServices,
  onsaVrfServices,
  notDeletableStates,
  retryableStates
} from "../site-constants.js";
import {
  ResourcesModal,
  ActivateModal,
  AccessNodeModal,
  TerminateModal,
  UnsubscribeModal
} from "../components/Modals";

import FormAlert from "../components/Form/FormAlert";
import { URLs, HTTPGet, ServiceURLs } from "../middleware/api.js";
import RetryModal from "../components/Modals/RetryModal.jsx";

class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      activateModal: false,
      accessNodeActivateModal: false,
      displayMessage: "",
      modalService: { id: null, type: null },
      resources: null,
      resourcesModal: false,
      retryModal: false,
      services: [],
      serviceChanged: null,
      successAlert: null,
      terminateModal: false,
      unsubscribeModal: false
    };
  }

  componentDidMount() {
    this.getServices();
    this.props.displayNavbar(false);
  }

  getServices() {
    HTTPGet(URLs["services"]).then(
      jsonResponse => this.setState({ services: jsonResponse }),
      error => this.showAlertBox(false, error.message)
    );
  }

  getOneService = serviceID =>
    new Promise((resolve, reject) => {
      HTTPGet(ServiceURLs("service", serviceID)).then(
        jsonResponse => {
          resolve(jsonResponse);
        },
        error => {
          reject(error);
        }
      );
    });

  showAlertBox = (result, message) => {
    this.setState({
      dialogSuccess: result,
      dialogText: message,
      dialogShow: message || result ? true : false
    });
  };

  handleOnClick = event => {
    const value = event.target.value;
    const name = event.target.name;

    let service = JSON.parse(value);

    this.setState({
      modalService: { id: service.id, type: service.service_type }
    });

    switch (name) {
      case "resources":
        let url = ServiceURLs("resources", service.id);

        HTTPGet(url).then(
          jsonResponse => {
            this.setState({
              resources: jsonResponse,
              resourcesModal: !this.state.resourcesModal
            });
          },
          error => {
            this.showAlertBox(false, error.message);
          }
        );

        break;
      case "activate":
        this.setState({
          activateModal: !this.state.accessNodeActivateModal
        });
        break;
      case "anActivate":
        this.setState({
          accessNodeActivateModal: !this.state.accessNodeActivateModal
        });
        break;
      case "retry":
        this.setState({
          // retryModal: !this.state.retryModal
          accessNodeActivateModal: !this.state.accessNodeActivateModal
});
        break;
      case "terminate":
        this.setState({
          terminateModal: !this.state.terminateModal
        });
        break;
      case "unsubscribe":
        this.setState({
          unsubscribeModal: !this.state.unsubscribeModal
        });
        break;
      default:
        break;
    }
  };

  handleToggle = (name, value, serviceChanged) => {
    let state = {
      [name]: !value,
      serviceChanged: serviceChanged
    };

    if (serviceChanged) {
      this.updateOneService(this.state.modalService.id);
    }

    this.setState(state);
  };

  updateOneService = serviceId => {
    let updatedServices = [];

    this.getOneService(serviceId).then(
      updatedService => {
        updatedServices = [...this.state.services];
        let selectedIndex = updatedServices.findIndex(
          x => x.id === serviceId
        );
        if ("msg" in updatedService) { // if key "msg" exists then the service was deleted.

          updatedServices.splice(selectedIndex, 1);
        } else {

          updatedServices[selectedIndex] = updatedService;
        }
        this.setState({ services: updatedServices });
      },
      error => this.showAlertBox(false, error.message)
    );
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
          {service.service_state === "in_construction" ? (
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
          {service.service_state === "an_activated" &&
          (onsaVrfServices.includes(service.service_type) ||
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
          {notDeletableStates.indexOf(service.service_state) === -1 ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="danger"
                name="unsubscribe"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
              >
                Unsubscribe
              </Button>
            </td>
          ) : null}
          {retryableStates.indexOf(service.service_state) !== -1 ? (
            <td>
              <Button
                className="btn btn-primary btn-sm btn-block"
                color="success"
                name="retry"
                onClick={this.handleOnClick}
                type="button"
                value={JSON.stringify(service)}
              >
                Retry
              </Button>
            </td>
          ) : null}
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
          alert={this.showAlertBox}
        />
        <RetryModal
          isOpen={this.state.retryModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
        />
        <TerminateModal
          isOpen={this.state.terminateModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
        />
        <UnsubscribeModal
          isOpen={this.state.unsubscribeModal}
          service={this.state.modalService}
          toggle={this.handleToggle}
          alert={this.showAlertBox}
        />
      </div>
    );
  }
}

export default Dashboard;
