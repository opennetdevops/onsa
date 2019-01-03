import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class SearchBox extends React.Component {

  static propTypes = {
    className: PropTypes.string,
  };

  static defaultProps = {
    className: "form-inline my-2 my-lg-0"
  };

  render() {

  	const { children,
  		    className,
            ...props
  		  } = this.props;

    return ( 	  
  		<form className={className}>
          <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
          <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
    );
  }
}

export default SearchBox;        



        <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>