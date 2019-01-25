import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...attributes }) => (
    <Route {...attributes} render={(props) => {
      let token = sessionStorage.getItem('token');
      console.log(token)
      if (token !== null) {
        return <Component {...props} displayNavbar={attributes.displayNavbar} />
      }
      else {
        return <Redirect to='/login' />
      }          
      }}/>
  )

export default PrivateRoute;