import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import NavbarBrand from './NavbarBrand';
import NavDropdown from './NavDropdown';
import DropdownMenu from './DropdownMenu';
import DropdownItem from './DropdownItem';
import NavbarToggler from './NavbarToggler';
import Nav from './Nav';
import NavLink from './NavLink';
import NavItem from './NavItem';
import Collapse from '../Collapse';

import logo from '../../images/logo.png'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

const Navbar = (props) => {
	const { className,
			bsSuffix,
			...attributes
		} = props

	return (
		<nav className={classNames(className,bsSuffix)} {...attributes}>
			<NavbarToggler data-toggle="collapse" data-target="#navbarCollapseTest" aria-controls="navbarCollapseTest" aria-expanded="false" aria-label="Toggle navigation"/>
			<Collapse bsSuffix="navbar-collapse" id="navbarCollapseTest">
			<Nav bsSuffix="mr-auto">
				<NavItem bsSuffix={props.history.location.pathname.includes('/dashboard') ? "active" : ""}>
					<NavLink bsSuffix="text-secondary" href="/dashboard"><FontAwesomeIcon icon="chart-line"/> Dashboard</NavLink>
				</NavItem>
				<NavDropdown bsSuffix={props.history.location.pathname.includes('/services') ? "active" : ""}>
					<NavLink bsSuffix="dropdown-toggle text-secondary" id="dropdown01" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><FontAwesomeIcon icon="bolt"/> Services</NavLink>
					<DropdownMenu>
						<DropdownItem href="/services/create">Create</DropdownItem>
					</DropdownMenu>
				</NavDropdown>
				<NavDropdown bsSuffix={props.history.location.pathname.includes('/customers') ? "active" : ""}>
					<NavLink bsSuffix="dropdown-toggle text-secondary" id="dropdown02" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><FontAwesomeIcon icon="male"/> Customers</NavLink>
					<DropdownMenu>
						<DropdownItem href="/customers/create">Add customer</DropdownItem>
						<DropdownItem href="/customerslocations">Add customer location</DropdownItem>
					</DropdownMenu>
				</NavDropdown>
				<NavDropdown bsSuffix={props.history.location.pathname.includes('/projects') ? "active" : ""}>
					<NavLink bsSuffix="dropdown-toggle text-secondary" id="dropdown03" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><FontAwesomeIcon icon="project-diagram"/> Projects</NavLink>
					<DropdownMenu>
						<DropdownItem href="/projects/create">Create project</DropdownItem>
						<DropdownItem href="/accessports">Add access port</DropdownItem>
						<DropdownItem href="/logicalunits">Add logical units</DropdownItem>
						<DropdownItem href="/vrfs">Add vrf</DropdownItem>
					</DropdownMenu>
				</NavDropdown>
			</Nav>
			</Collapse> 
			<NavbarBrand bsSuffix="navbar-center text-secondary" href="/dashboard"><img className="xlogo" alt="" src={logo}/></NavbarBrand>
			<Nav bsSuffix="ml-auto">
				<NavLink bsSuffix="text-secondary" href="/login"><FontAwesomeIcon icon="sign-out-alt"/> Logout</NavLink>
			</Nav>
		</nav>
		);
}

Navbar.propTypes = {
	className: PropTypes.string,
	bsSuffix: PropTypes.string
}

Navbar.defaultProps = {
	className: "navbar",
	bsSuffix: "navbar navbar-expand-md navbar-dark bg-white fixed-top border-bottom",
}

export default Navbar;