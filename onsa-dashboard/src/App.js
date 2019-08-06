import React from 'react';
import { Router, Route, Switch, Redirect } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import { publicRoutes, privateRoutes } from "./routes/index.js";
import Navbar from './components/Navbar';
import Tag from './components/Tag';
import Footer from './components/Footer';
import PrivateRoute from './components/PrivateRoute';
import './css/fibercorp-labs.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChartLine, faBolt, faMale, faProjectDiagram, faSignOutAlt } from '@fortawesome/free-solid-svg-icons'

library.add(faChartLine, faBolt, faMale, faProjectDiagram, faSignOutAlt)

var hist = createBrowserHistory();

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLogin: true,
      whoIsActive: null
    };
  }

  handleNavbar = (value) => {
    this.setState({'isLogin': value});
  }
//Test comment - - delete it
  render() {

    return (

      <React.Fragment>
      {this.state.isLogin ? null : <Navbar history={hist}/>}
      <Tag tag="main" role="main">
      <Router history={hist}>
        <Switch>
          {publicRoutes.map((prop, key) => {
            return <Route path={prop.path} key={key} render={(props) => <prop.component {...props} displayNavbar={this.handleNavbar}/>}/>;
          })}
          {privateRoutes.map((prop, key) => {
            return <PrivateRoute component={prop.component} path={prop.path} key={key} displayNavbar={this.handleNavbar}/>;
          })}
          <Redirect exact from='/' to='/login'/>
        </Switch>
      </Router>
      </Tag>
      {this.state.isLogin ? <Footer/> : null}
      </React.Fragment>
    );
  }
}

export default App;