import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...attributes }) => (
    <Route {...attributes} render={(props) => {
      let token = sessionStorage.getItem('token');
      if (token === null || token == 'invalid') {
        return <Redirect to='/login' />
      }
      else {
        return <Component {...props} displayNavbar={attributes.displayNavbar} />
      }          
      }}/>
  )

export default PrivateRoute;