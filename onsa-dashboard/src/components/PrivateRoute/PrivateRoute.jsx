import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...attributes }) => (
    <Route {...attributes} render={(props) => {
      
      let token = sessionStorage.getItem('token');
      if (token === null || token === 'invalid') {
        console.log("Token = NULL")
        return <Redirect to='/login' />
      }
      else {
        console.log("Token = OK")

        return <Component {...props} displayNavbar={attributes.displayNavbar} />
      }          
      }}/>
  )

export default PrivateRoute;