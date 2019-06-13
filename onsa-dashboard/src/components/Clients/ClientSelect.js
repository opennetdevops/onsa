import React, { Component } from 'react';
import AsyncSelect from 'react-select/lib/Async';
import { URLs, HTTPGet } from "../../middleware/api";

 class ClientSelect extends Component {
   
  clientList = inputValue =>
     new Promise((resolve,reject) => {
      if (inputValue.length >= this.props.searchByMT) {
        let url = URLs["clients"] + "?search=" + inputValue;

        resolve(
          HTTPGet(url).then(
            jsonResponse => {
              return jsonResponse.map(client => {
                return { value: client.id, label: client.name };
              });
            },
            error => {
              reject(this.props.errorMsg(false, error.message)
                );
            }
          )
        );
      }
     }); 

   render() {
     
     return (
       <AsyncSelect
         loadOptions={this.clientList}
         isClearable
         onChange={this.props.onChange}
         value={this.props.value}
         placeholder={
           "Search by " + this.props.searchByMT + " or more letters"
         }
         name={this.props.name}
       />
     );
   }
 };

  export default ClientSelect;