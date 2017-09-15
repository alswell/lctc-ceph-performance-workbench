/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Button } from 'antd'
import TestForm from './ReRunForm'
import { fetchAndNotification } from '../../services/restfulService'

export class ReRunPage extends React.Component {

  componentDidMount () {
    
  }

  saveFormRef = (form) => {
    this.form = form
  };

  render () {
    return (
      <span>
        <TestForm
          ref={this.saveFormRef}
          visible={this.props.visible}
          onCancel={this.props.onCancel}
          refresh={this.props.refresh}
          record={this.props.record}
        />
      </span>
    )
  }
}
