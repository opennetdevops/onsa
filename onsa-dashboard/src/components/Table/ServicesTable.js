import React, { Component } from 'react';
import { forwardRef } from 'react';


import Spinner from "../UI/Spinner/Spinner";
import { notDeletableStates, retryableStates } from "../../site-constants"

import MaterialTable from "material-table";

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
import Refresh from '@material-ui/icons/Refresh';
import ViewColumn from '@material-ui/icons/ViewColumn';
import Loop from '@material-ui/icons/Loop';
import Settings from "@material-ui/icons/Settings"
import SettingsPower from "@material-ui/icons/SettingsPowerRounded"

 
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
    tableRef = React.createRef();

    render() {
        return ( 
          <MaterialTable
            tableRef={this.tableRef}

            icons={tableIcons}
            columns={[
              { title: "Product ID", field: "id" },
              { title: "GTS", field: "gts_id" },
              { title: "Service Type", field: "service_type" },
              { title: "State", field: "service_state" },
              { field: "isUpdating", searchable: false, 
                render: rowdata =>
                  rowdata.isUpdating ? <Spinner /> : null
              }
            ]}
            data={this.props.services}
            detailPanel={[{ 
                tooltip:" View Resources", 
               render: rowData => {
               return (
                 <div style={{ textAlign: "center" }}>
                   {" "}
                   <h4>Resources.. service Id: {rowData.id}</h4>{" "}
                 </div>
               );
             }}]}  
             title="Services"
             actions={[
               // config SCO
               rowdata => ({
                 icon: () => <Settings />,
                 tooltip: "Configure SCO",
                 onClick: (event, rowData) =>
                   alert("Configure SCO for service Id:  " + rowData.id),
                 disabled: rowdata.service_state !== "in_construction"
               }),
               // Unsubscribe
               rowdata => ({
                 icon: () => <RemoveCircle />,
                 tooltip: "Unsubscribe service",
                 onClick: (event, rowData) =>
                   alert("Unsubscribe service Id:  " + rowData.id),
                 disabled: notDeletableStates.includes(
                   rowdata.service_state
                 )
               }),
               // Terminate
               rowdata => ({
                 icon: () => <SettingsPower />,
                 tooltip: "Terminate",
                 // onClick: (event, rowData) =>
                 //   alert("Terminate service Id:  " + rowData.id),
                 disabled: !(rowdata.service_state === "an_activated")
               }),
               //Retry
               rowdata => ({
                 icon: () => <Loop />,
                 tooltip: "Retry!",
                 onClick: (event, rowData) =>
                   alert("Retry service Id:  " + rowData.id),
                 disabled: !retryableStates.includes(
                   rowdata.service_state
                 )
               }),
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
               filtering: false
             }}
           />
         );
 
     }
}

export default ServicesTable;
