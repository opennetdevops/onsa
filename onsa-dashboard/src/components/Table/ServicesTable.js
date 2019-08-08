import React, { Component } from 'react';
import Spinner from "../UI/Spinner/Spinner";
import {
  notDeletableStates,
  retryableStates,
  serviceStatesEnum,
  serviceEnum
} from "../../site-constants";
import { lowerCase, startCase } from 'lodash';
import ResourcesDetailRow from './ServicesTableComponents/ResourcesDetailRow'

//import Table - Icons:
import AddBox from '@material-ui/icons/AddBox';
import ArrowUpward from '@material-ui/icons/ArrowUpward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import RemoveCircle from '@material-ui/icons/DeleteRounded';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
// import Refresh from '@material-ui/icons/Refresh';
import ViewColumn from '@material-ui/icons/ViewColumn';
import Loop from '@material-ui/icons/Loop';
import Settings from "@material-ui/icons/Settings"
import SettingsPower from "@material-ui/icons/SettingsPowerRounded"

// import { createMuiTheme } from '@material-ui/core/styles';
// import { ThemeProvider } from '@material-ui/styles';

import MaterialTable from 'material-table';
import classes from "./ServiceTable.module.css";

// const themeTable = createMuiTheme({
//   overrides: {
//     MuiTableCell: {
//       root: {
//         "&:hover": {
//           backgroundColor: "rgba(33, 150, 243, 0.5)"
//         }
//       }
//     }
//   }
// });


const tableIcons = {
    Add: () => <AddBox />,
  Check: () => <Check />,
  Clear: () => <Clear />,
  Delete: () => <DeleteOutline />,
  DetailPanel: () => <ChevronRight />,
  Edit: () => <Edit />,
  Export: () => <SaveAlt />,
  Filter: () => <FilterList />,
  FirstPage: () => <FirstPage />,
  LastPage: () => <LastPage />,
  NextPage: () => <ChevronRight />,
  PreviousPage: () => <ChevronLeft />,
  ResetSearch: () => <Clear />,
  Search: () => <Search />,
  SortArrow: () => <ArrowUpward />,
  ThirdStateCheck: () => <Remove />,
  ViewColumn: () => <ViewColumn />
  };

const cellStyle =      {
  paddingTop: "0.5rem",
  paddingRight:"1rem ",
  paddingBottom: "0.5rem",
  paddingLeft: "1rem",
  textAlign:"left",
  
} 
const cellStyleSmall = { 
  ...cellStyle, paddingRight:"0.5rem", paddingLeft:"2rem", textAlign:"left"//, backgroundColor:"#eee"
} 
const headerStyleSmall = {
  ...cellStyleSmall, textAlign:"left"
}
const headerStyleLarge = {
  ...cellStyle
}
const headerStyleXL = {
  ...cellStyle, width: "15rem"
}

class ServicesTable extends Component {
  tableRef = React.createRef();
  
  state = {
    mappedServices: []
  }

  componentDidMount() {
    console.log("[Table DidMount:] ");
  }

  componentDidUpdate(prevProps) {
    console.log("[Table DidUpdate:] ");
    if (prevProps.services !== this.props.services  ) {
      this.setState({mappedServices: this.mapServicesName(this.props.services)})
    }

  }
  shouldComponentUpdate(nextProps, nextState) {
    if (
      nextProps.services !== this.props.services ||
      nextState.mappedServices !== this.state.mappedServices
    ) {
      console.log(" -- SERVICES CHANGED -- ");
      return true;
    }
    if (nextProps.updatingServices !== this.props.updatingServices) {
      // console.log(" -- UpdatingLIST CHANGED -- ")
      return true;
    }
    return false;
  }

  mapServicesName = services => {
    const servicesMappedNames = services.map(serv => {
      return this.mapServiceName(serv);
    });
    return servicesMappedNames;
  };
  mapServiceName = service => {
    let newServ = { ...service };
    newServ.service_type = serviceEnum[service.service_type];
    newServ.originalServState = service.service_state;
    newServ.service_state = startCase(
      lowerCase(serviceStatesEnum[service.service_state])
    );
    if ("client__name" in newServ) {
      newServ.client__name =
        service.client__name.length < 40
          ? service.client__name
          : service.client__name.substring(0, 40).concat("..");
    }
    newServ.newBW = newServ.bandwidth == null ? "-" : newServ.bandwidth;
    newServ.newGTS = newServ.gts_id == null ? "-" : newServ.gts_id;
    return newServ;
  };

  render() {
    // const updatingService = !this.props.updatingServices.length;
    console.log( "[Table Render], services: " );

    return (
      <div className={classes.tableWrapper}>
        <MaterialTable
          style={classes.servicesTable}
          tableRef={this.tableRef}
          icons={tableIcons}
          columns={[
            {
              title: "CUIC",
              field: "client__cuic",
              cellStyle: cellStyle,
              headerStyle: headerStyleLarge
            },
            {
              title: "Client Name",
              field: "client__name",
              cellStyle: cellStyle,
              headerStyle: headerStyleXL
            },
            {
              title: "Product",
              field: "id",
              cellStyle: cellStyle,
              headerStyle: headerStyleLarge
            },
            {
              title: "GTS",
              field: "gts_id",
              cellStyle: cellStyle,
              headerStyle: headerStyleLarge
            },
            {
              title: "Service Type",
              field: "service_type",
              grouping: false,
              cellStyle: cellStyleSmall,
              headerStyle: headerStyleSmall
            }, //, lookup: serviceEnum
            {
              title: "BW [mbps]",
              field: "bandwidth",
              grouping: false,
              cellStyle: cellStyleSmall,
              headerStyle: headerStyleSmall,
              customSort: (a, b) => a.bandwidth - b.bandwidth
            },
            {
              title: "State    ",
              field: "service_state",
              grouping: false,
              cellStyle: cellStyle,
              headerStyle: cellStyle
            }, //, lookup: serviceStatesEnum },
            {
              field: "isUpdating",
              searchable: false,
              // defaultSort: "desc",
              filtering: false,
              export: false,
              cellStyle: cellStyleSmall,
              headerStyle: headerStyleSmall,
              grouping: false,
              render: rowdata =>
                this.props.updatingServices.some(e => e.id === rowdata.id) ? (
                  <Spinner />
                ) : null
            }
          ]}
          data={this.state.mappedServices}
          detailPanel={[
            {
              tooltip: " View Resources",
              render: rowData => {
                return (
                  <div style={{ textAlign: "center" }}>
                    <ResourcesDetailRow
                      serviceData={rowData}
                      alert={this.props.alert}
                    />
                  </div>
                );
              }
            }
          ]}
          title="Services Dashboard"
          isLoading={this.props.isLoadingServices}
          actions={[
            // config SCO
            rowdata => ({
              icon: () => <Settings />,
              tooltip: "Configure SCO",
              onClick: (event, rowData) =>
                this.props.onClickedAction(
                  "anActivate",
                  rowData.id,
                  rowData.service_type
                ),
              disabled:
                rowdata.originalServState !== "in_construction" ||
                rowdata.isUpdating
            }),

            // Terminate
            rowdata => ({
              icon: () => <SettingsPower />,
              tooltip: "Terminate",
              onClick: (event, rowData) =>
                this.props.onClickedAction(
                  "terminate",
                  rowData.id,
                  rowData.service_type
                ),

              disabled:
                rowdata.originalServState !== "an_activated" ||
                rowdata.isUpdating
            }),
            // Unsubscribe
            rowdata => ({
              icon: () => <RemoveCircle />,
              tooltip: "Unsubscribe service",
              onClick: (event, rowData) => {
                this.props.onClickedAction(
                  "unsubscribe",
                  rowData.id,
                  rowData.service_type,
                  rowData.service_state
                );
              },

              disabled:
                notDeletableStates.includes(rowdata.originalServState) ||
                rowdata.isUpdating ||
                rowdata.service_type === "Legacy"
            }),
            //Retry
            rowdata => ({
              icon: () => <Loop />,
              tooltip: "Retry!",
              onClick: (event, rowData) =>
                this.props.onClickedAction(
                  "retry",
                  rowData.id,
                  rowData.service_type
                ),

              disabled:
                !retryableStates.includes(rowdata.originalServState) ||
                rowdata.isUpdating
            })

            //refresh all
            // {
            //   icon: () => <Refresh />,
            //   tooltip: "Refresh Data",
            //   isFreeAction: true,
            //   onClick: (event, rowData) =>  this.props.refreshData()
            // }
          ]}
          options={{
            actionsColumnIndex: -1,
            search: true,
            filtering: false,
            sorting: true,
            exportButton: true,
            grouping: false, //updatingService
            pageSize: 5,
            pageSizeOptions: [5, 10, 20, 50],
            emptyRowsWhenPaging: false,
            exportAllData: true,
            headerStyle: {
              backgroundColor: "#2b587ab7", 
              color: "#FFF",
              fontFamily: "Oswald",
              fontWeight: 400,
              fontSize: "18px",
              textAlign: "center"
            },
            rowStyle: {
              fontFamily: "Titillium Web"
            }
          }}
        />
      </div>
    );
  }
}

export default ServicesTable;
