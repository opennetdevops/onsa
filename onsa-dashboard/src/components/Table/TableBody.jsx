import React from 'react';
import PropTypes from 'prop-types';

class TableBody extends React.Component {

  static propTypes = {
    id: PropTypes.string,
    className: PropTypes.string
  };

  render() {

    const { children,
            id,
            className,
            ...props

          } = this.props

    return (
	  <tbody>
	  	{children}
	  </tbody>

    );
    }
}

export default TableBody;