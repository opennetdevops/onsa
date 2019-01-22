import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...attributes }) => (
    <Route {...attributes} render={(props) => (
      true === true
        ? <Component {...props} displayNavbar={attributes.displayNavbar} />
        : <Redirect to='/login' />
    )} />
  )

export default PrivateRoute;