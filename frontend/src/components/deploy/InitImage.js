/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col, Select } from 'antd'
import PropTypes from 'prop-types'
import './TestForm.less'
import TestForm from './InitImageForm'

const FormItem = Form.Item

export class InitImagePage extends React.Component {
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
        <Button type="primary" onClick={this.showModal}>Init Image</Button>
        <TestForm
          ref={this.saveFormRef}
          visible={this.state.visible}
          onCancel={this.handleCancel}
          onCreate={this.handleCreate}
          refresh={this.props.refresh}
        />
      </span>
    )
  }
}