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
import RemoveCircle from '@material-ui/icons/RemoveCircle';
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

class ServicesTable extends Component { 

      // componentDidMount() {
    //     console.log("[Table DidMount:] ", this.props)
    // }

    componentDidUpdate() {
        // console.log("[Table DidUpdate:] ")
    }

    render() {
      //
        const servicesMappedNames = this.props.services.map(serv => {
        let newServ= {...serv}
        newServ.service_type =  serviceEnum[serv.service_type]
        newServ.originalServState = serv.service_state
        newServ.service_state = startCase(lowerCase(serviceStatesEnum[serv.service_state]))
        newServ.newBW = serv.bandwidth + " Mbps"
        return newServ
      })
        return (
          <div className={classes.tableWrapper}>
          <MaterialTable
            icons={tableIcons}
            columns={[
              { title: "Product", field: "id" },
              { title: "GTS", field: "gts_id" },
              { title: "Service Type", field: "service_type"}, //, lookup: serviceEnum
              { title: "BW", field: "newBW"}, 
              { title: "State    ", field: "service_state"}, //, lookup: serviceStatesEnum },
              {
                field: "isUpdating",
                searchable: false,
                filtering:false,
                export:false,
                render: rowdata =>
                  rowdata.isUpdating ? <Spinner /> : null
              }
            ]}
            data={servicesMappedNames}
            detailPanel={[
              {
                tooltip: " View Resources",
                render: rowData => {
                  return (
                    <div style={{ textAlign: "center" }}>
                      <ResourcesDetailRow serviceData={rowData} alert={this.props.alert}
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
              // Unsubscribe
              rowdata => ({
                icon: () => <RemoveCircle />,
                tooltip: "Unsubscribe service",
                onClick: (event, rowData) =>
                  this.props.onClickedAction(
                    "unsubscribe",
                    rowData.id,
                    rowData.service_type,
                    rowData.service_state
                  ),

                disabled:
                  notDeletableStates.includes(rowdata.originalServState) ||
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
              //    {
              //      icon: () => <Refresh/>,
              //      tooltip: 'Refresh Data',
              //      isFreeAction: true,
              //     //  onClick: this.tableRef.current && this.tableRef.current.onQueryChange()
              //    }
            ]}
            options={{
              actionsColumnIndex: -1,
              search: true,
              filtering: true,
              exportButton: true,
              grouping:true,
              pageSizeOptions:[5,10,20,50 ],
              headerStyle: {
                backgroundColor: "#346c97", // '#01579b',
                color: '#FFF',
                fontFamily:"Oswald",
                fontWeight:400,
                fontSize: "18px",
                textAlign: "center",
              },
              rowStyle: {
                fontFamily: 'Titillium Web',
                fontSize: "16px"
              }
            }}
          />
          </div>
        );
 
     }
}

export default ServicesTable;
