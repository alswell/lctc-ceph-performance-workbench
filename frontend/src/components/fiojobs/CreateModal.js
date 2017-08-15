/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Button } from 'antd'
import TestForm from './TestForm'

export class CollectionsPage extends React.Component {
  state = {
    visible: false,
  };
  showModal = () => {
    this.setState({ visible: true })
  };
  handleCancel = () => {
    this.setState({ visible: false })
  };
  handleCreate = () => {
    const form = this.form
    form.validateFields((err, values) => {
      if (err) {
        return
      }

      console.log('Received values of form: ', values)
      form.resetFields()
      this.setState({ visible: false })
    })
  };
  saveFormRef = (form) => {
    this.form = form
  };

  render () {
    return (
      <span>
        <Button type="primary" onClick={this.showModal}>Create</Button>
        <TestForm
          ref={this.saveFormRef}
          visible={this.state.visible}
          onCancel={this.handleCancel}
          onCreate={this.handleCreate}
        />
      </span>
    )
  }
}
