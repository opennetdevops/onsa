import React from 'react';
import PropTypes from 'prop-types';

class TableHead extends React.Component {

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
      <thead>
        <tr>
          <th className="th-sm">Client
            <i class="fa fa-sort float-right" aria-hidden="true"></i>
          </th>
          <th className="th-sm">Service
            <i className="fa fa-sort float-right" aria-hidden="true"></i>
          </th>
          <th className="th-sm">Product Id
            <i className="fa fa-sort float-right" aria-hidden="true"></i>
          </th>
          <th className="th-sm">Number of CPEs
            <i className="fa fa-sort float-right" aria-hidden="true"></i>
          </th>
        </tr>
      </thead>

    );
    }
}

export default TableHead;