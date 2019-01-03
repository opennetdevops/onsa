import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class Table extends React.Component {

  static propTypes = {
    id: PropTypes.string,
    className: PropTypes.string
  };

  static defaultProps = {
    className: "table table-striped table-bordered table-sm"
  };


  render() {

    const { children,
            id,
            className,
            ...props

          } = this.props

    return (
      <table id={id} className={classNames(className)} cellspacing="0" width="100%">
        {children}
      </table>

    );
    }
}

export default Table;